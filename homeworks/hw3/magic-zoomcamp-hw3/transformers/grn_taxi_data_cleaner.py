if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    # Specify your transformation logic here
    print(f'Preprocessing: of {data.shape[0]}, there are {data.query("passenger_count == 0 | trip_distance == 0").shape[0]} records with no passenger count or trip distance of 0')
    # filter out unwanted rows 
    df = data.query("passenger_count > 0").query("trip_distance > 0")

    # change all col names to snake syntax
    print(f"need to change the following columns to snake case: {', '.join(df.columns[df.columns.str.contains('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', regex = True)])}")

    df.columns = df.columns\
                .str.replace('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', '_', regex=True)\
                .str.lower()

    print(f'exporting a df with {df.shape[0]} records')
    
    return df


@test
def test_passenger_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'

@test
def test_distance_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero travel distance'

@test 
def test_camel_col_name(output, *args) -> None:
    assert len(output.columns[output.columns.str.contains('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', regex = True)]) == 0, 'The column names are not in snake format'