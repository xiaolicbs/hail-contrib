from hail import TStruct, VariantDataset
from hail.typecheck import typecheck, anytype

@typecheck(vds=VariantDataset,
           f=anytype)
def mutate_va_schema(vds, f):
    """Apply a lambda function to each variant annotation name.

    **Examples**

    Lower-case each element in variant schema:

    >>> vds = mutate_va_schema(vds, lambda x: x.lower())

    Replace all instances of '.' with '__':

    >>> vds = mutate_va_schema(vds, lambda x: x.replace('.', '__'))

    **Notes**

    This method uses ``annotate_variants_expr`` to rename all variant annotations
    using the function supplied.
    
    :param vds: Dataset to modify.
    :type vds: VariantDatset

    :param f: Function to apply to schema identifiers.
    :type f: str => str

    :returns: Datset with modified variant schema.
    :rtype: VariantDataset
    """

    # if va is not a struct, return the VDS (no need to mutate)
    if not isinstance(vds.variant_schema, TStruct):
        return vds

    # the below function is called on structs to recursively generate the expr
    def generate_struct_expr(schema, prefix):
        assert isinstance(schema, TStruct)

        exprs = []
        for field in schema.fields:
            name = field.name
            typ = field.typ
            full_name = prefix + '.`{}`'.format(name)
            mutated = f(name)
            if isinstance(typ, TStruct):
                right_hand = generate_struct_expr(typ, full_name)
            else:
                right_hand = full_name
            exprs.append('`{}`: {}'.format(mutated, right_hand))
        return '{' + ','.join(exprs) + '}'

    va_expr = generate_struct_expr(vds.variant_schema, 'va')
    return vds.annotate_variants_expr('va = {}'.format(va_expr))


@typecheck(vds=VariantDataset,
           f=anytype)
def mutate_sa_schema(vds, f):
    """Apply a lambda function to each sample annotation name.

    **Examples**

    Lower-case each element in sample schema:

    >>> vds = mutate_sa_schema(vds, lambda x: x.lower())

    Replace all instances of '.' with '__':

    >>> vds = mutate_sa_schema(vds, lambda x: x.replace('.', '__'))

    **Notes**

    This method uses ``annotate_variants_expr`` to rename all variant annotations
    using the function supplied.

    :param vds: Dataset to modify.
    :type vds: VariantDatset

    :param f: Function to apply to schema identifiers.
    :type f: str => str

    :returns: Datset with modified sample schema.
    :rtype: VariantDataset
    """

    # if sa is not a struct, return the VDS (no need to mutate)
    if not isinstance(vds.sample_schema, TStruct):
        return vds

    # the below function is called on structs to recursively generate the expr
    def generate_struct_expr(schema, prefix):
        assert isinstance(schema, TStruct)

        exprs = []
        for field in schema.fields:
            name = field.name
            typ = field.typ
            full_name = prefix + '.`{}`'.format(name)
            mutated = f(name)
            if isinstance(typ, TStruct):
                right_hand = generate_struct_expr(typ, full_name)
            else:
                right_hand = full_name
            exprs.append('`{}`: {}'.format(mutated, right_hand))
        return '{' + ','.join(exprs) + '}'

    sa_expr = generate_struct_expr(vds.sample_schema, 'sa')
    return vds.annotate_samples_expr('sa = {}'.format(sa_expr))
