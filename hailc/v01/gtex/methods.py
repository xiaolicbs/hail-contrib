from hail.typecheck import typecheck, anytype
import types


def filter_gatk_intervals(self, interval, keep):
    """ Filter VariantDataset with an interval file in GATK's format

    **Examples**

    >>> vds_results = vds.filterGatkIntervals(interval_file, keep=True)
    Keep variants in the interval file.

    **Notes**

    :param interval: an interval file
    :return
    :rtype a VariantDatset with modified sites

    """
    self = (self.filter_variants_table(
            KeyTable.import_interval_list(interval), keep=keep))
    return self


def remove_monomorphic(self):
    """ Perform re-calculate allele frequencies with variant qc
        and remove monomorphic sites from a VDS

    **Examples**

    >>> vds_results = vds.remove_monomorphic()

    **Notes**

    """
    self = (self
            .variant_qc()
            .filter_variants_expr('v.alt=="*" || va.qc.AC==0 \
                                  || va.qc.nCalled*2==va.qc.AC',
                                  keep=False)
            .annotate_variants_expr('va.info.AC=va.qc.AC, \
                                     va.info.AN=2 * va.qc.nCalled, \
                                     va.info.AF=va.qc.AF'))
    return self


def summarize_vds(self, split=True, chrX='chrX'):
    """ Query the VDS and return summary statistics

    (vds, summary) = vds.summarize_vds()

    **examples**

    **notes**

    """
    if split:
        title = ['Total', 'SNP', 'InDel', 'Split', 'MAF01', 'MAF05',
                 'xTotal', 'xSNP', 'xInDel', 'xSplit', 'xMAF01', 'xMAF05']
        queries = [
            'variants.count()',
            'variants.filter(v => v.altAllele.isSNP()).count()',
            'variants.filter(v => v.altAllele.isIndel()).count()',
            'variants.filter(v => va.wasSplit).count()',
            'variants.filter(v => va.qc.AF > 0.01 \
                             && va.qc.AF < 0.99).count()',
            'variants.filter(v => va.qc.AF > 0.05 \
                             && va.qc.AF < 0.95).count()',
            'variants.filter(v => v.contig == "{}").count()'.format(chrX),
            'variants.filter(v => v.altAllele.isSNP() \
                             && v.contig == "{}").count()'.format(chrX),
            'variants.filter(v => v.altAllele.isIndel() \
                             && v.contig == "{}").count()'.format(chrX),
            'variants.filter(v => va.wasSplit \
                             && v.contig == "{}").count()'.format(chrX),
            'variants.filter(v => va.qc.AF > 0.01 && va.qc.AF < 0.99 \
                             && v.contig == "{}").count()'.format(chrX),
            'variants.filter(v => va.qc.AF > 0.05 && va.qc.AF < 0.95 \
                             && v.contig == "{}").count()'.format(chrX)
        ]
    else:
        title = ['Total', 'SNP', 'InDel', 'Split', 'MAF01', 'MAF05',
                 'xTotal', 'xSNP', 'xInDel', 'xSplit', 'xMAF01', 'xMAF05']
        queries = [
            'variants.count()',
            'variants.filter(v => v.isBiallelic).count()',
            'variants.filter(v => va.info.AF.sum() > 0.01 \
                             && va.info.AF.sum() < 0.99).count()',
            'variants.filter(v => va.info.AF.sum() > 0.05 \
                             && va.info.AF.sum() < 0.95).count()',
            'variants.filter(v => v.contig == "{}").count()'.format(chrX),
            'variants.filter(v => v.isBiallelic() \
                             && v.contig == "{}").count()'.format(chrX),
            'variants.filter(v => va.info.AF.sum() > 0.01 \
                             && va.info.AF.sum() < 0.99 \
                             && v.contig == "{}").count()'.format(chrX),
            'variants.filter(v => va.info.AF.sum() > 0.05 \
                             && va.info.AF.sum() < 0.95 \
                             && v.contig == "{}").count()'.format(chrX)
        ]
    print(' '.join(title))
    print(self.query_variants(queries))
    return(self)


def cal_genot_posteriors(self, ref):
    """ Calculate genotype posteriors given a reference panel
    **Examples**

    >>> vds_results = vds.calculate_genotype_posteriors()

    **Notes**

    :return A modified VariantDataset with a PP field for each genotype
    :rtype VariantDataset

    """
    return self


def add_filter(self):
    """
    **Examples**

    **Notes**

    """
    self = (self.annotate_variants_expr(
                'va.filters = if (isDefined(va.info.pHMISS) \
                                && va.info.pHMISS < 1e-8) \
                                va.filters.add("HMISSp08") \
                              else va.filters'))
    return self


def flag_removed_sites(self, vds_before, vds_after, flag):
    """ Add flag to va.filters of sites that were removed during variant
        quality control, by comparing vds before and after variant QC.

        **Examples**

        Add 'MISS15' as filter field for sites didn't contained in vds_after
        >>> vds_new = vds.flag_removed_sites(vds_before, vds_after,
                                             'MISS15')

        **Notes**

        :param vds_before: dataset before variant QC
        :type vds: VariantDataset

        :param vds_after: dataset after variant QC
        :type vds: VariantDataset

        :returns: Dataset with modified ``va.filters``
        :rtype: VariantDataset

    """
    # flag removed sites
    flag_sites_expr = 'va.filters = if (isDefined(vds)) va.filters \
                                    else va.filters.add("{}")'.format(flag)
    # only keep flagged sites
    vds_before = (vds_before
                  .annotate_variants_vds(vds_after,
                                         expr=flag_sites_expr)
                  .filter_variants_expr('va.filters.isEmpty', keep=False))
    # update VDS annotation
    update_vds_expr = 'va.filters = if (isDefined(vds)) vds.filters.union(va.filters) \
                                   else va.filters'
    self = self.annotate_variants_vds(vds_before, update_vds_expr)
    return self


def head(self, len=50):
    """ Show the head of a VariantDataset

    """
    self.variants_table().show(len)
    self.head = types.MethodType(head, self)


def remove_va_filter(self, flag):
    # remove VQSR tranches from the VDS
    expr = 'va.filters = if (va.filters.contains("{0}")) \
                            va.filters.filter(s => s != "{0}") \
                         else va.filters'.format(flag)
    return self.annotate_variants_expr(expr)


def patch():
    """  Do monkey patching
    ** Notes **
    """
    from hail.dataset import VariantDataset
    VariantDataset.flag_removed_sites = flag_removed_sites
    VariantDataset.head = head
    VariantDataset.remove_monomorphic = remove_monomorphic
    VariantDataset.summarize_vds = summarize_vds
    VariantDataset.remove_va_filter = remove_va_filter
