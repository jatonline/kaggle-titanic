from sklearn.base import BaseEstimator, TransformerMixin

    
def add_totals(ax):
    total = sum(patch.get_height() for patch in ax.patches)
    for patch in ax.patches:
        t = ax.annotate(
            f"{patch.get_height()}\n{patch.get_height() / total:0.0%}",
            xy=(
                patch.get_x() + patch.get_width() / 2,
                patch.get_y() + patch.get_height() + 10,
            ),
            ha="center",
            va="bottom",
        )

        
def add_rates(ax):
    total = sum(patch.get_height() for patch in ax.patches)
    for patch in ax.patches:
        t = ax.annotate(
            f"{patch.get_height():0.0%}",
            xy=(
                patch.get_x() + patch.get_width(),
                patch.get_y() + patch.get_height() + 0.01,
            ),
            ha="right",
            va="bottom",
        )


class AddFeature(TransformerMixin, BaseEstimator):
    def __init__(self, feature_name, feature_func, enabled=True):
        """Add a feature by applying a function to the dataset.
        
        Args
        ====
            feature_name : str
                The name of the columns to add.
                
            feature_func : callable
                A function that will return the new column of data. This should take
                the entire DataFrame is its only argument.
                
            enabled : bool (default=True)
                Whether to execute the transofrmer during the pipeline.
            
        Returns
        =======
            Dataset with rows dropped.
        """
        self.feature_name = feature_name
        self.feature_func = feature_func
        self.enabled = enabled
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if self.enabled:
            return X.assign(**{
                self.feature_name: self.feature_func(X),
            })
        else:
            return X
