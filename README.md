vetiver reprex for using custom elements
===

Per https://rstudio.github.io/vetiver-python/stable/custom_code.html "Deploying custom elements" we expect that the app defined in [attempt #2](attempt-2/api/app.py) should work. Instead, we need to add a custom element to the `__main__` namespace as in [attempt #3](attempt-3/api/app.py). The difference in the last line in:

```python
class MyTransformer(TransformerMixin, BaseEstimator):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X

# added to attempt #3, fixing the API
setattr(sys.modules["__main__"], "MyTransformer", MyTransformer)
```