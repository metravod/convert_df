# ConvertDF

A small class that will help you make the pandas dataframe serialization process more controllable.

```python
data = [[12, 'foo', 567.53], [45, 'bar', 421.3], [35, 'baz', 1321.5]]
cols = ['int_col', 'str_col', 'float_col']
df = pd.DataFrame(data, columns=cols)

ConvertDF(
    df.loc[:0], 
    rename_cols={'int_col': 'ids', 'str_col': 'type', 'float_col': 'value'}, 
    type_cols={'int_col': str, 'float_col': int},
    is_oneliner=True
).to_dict()

>>> {'ids': '12', 'type': 'foo', 'value': 567}
```