import numpy
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.linear_model import LinearRegression
from catboost import CatBoostRegressor
from sklearn.neighbors import NearestNeighbors
from kolibri.distances.heom import HEOM
from kolibri.distances.hvdm import HVDM
from kolibri.automl.data_inspection import get_data_info
import category_encoders as ce
from tqdm import tqdm

class LazyRegression(BaseEstimator, RegressorMixin):
    """
    Fits a linear regression, on sub sample of size n. The sample formed by the top n similar items to the
    sample to be predicted
    """


    def __init__(self, n_neighbors:int=10, algorithm='auto',  distance='heom', leaf_size:int=30, weight_by_distance=False):
        "constructor"
        RegressorMixin.__init__(self)
        BaseEstimator.__init__(self)
        self.estimator = CatBoostRegressor()
        self.algorithm=algorithm
        self.leaf_size=leaf_size
        self.n_neighbors=n_neighbors
        self.neigberhood=NearestNeighbors(n_neighbors=n_neighbors, algorithm=algorithm, leaf_size=leaf_size)
        self.weight_by_distance=weight_by_distance
        self.encoder=None
        self.distance=distance
    def fit(self, X, y):
        """
        Builds the tree model.
        :param X: numpy array or sparse matrix of shape [n_samples,n_features]
            Training data
        :param y: numpy array of shape [n_samples, n_targets]
            Target values. Will be cast to X's dtype if necessary
        :param sample_weight: numpy array of shape [n_samples]
            Individual weights for each sample
        :return: self : returns an instance of self.
        Fitted attributes:
        * `classes_`: classes
        * `tree_`: tree structure, see @see cl _DecisionTreeLogisticRegressionNode
        * `n_nodes_`: number of nodes
        """


        #convert to Dataframe if X is not a Dataframe
        if not isinstance(X, pd.DataFrame):
            X=pd.DataFrame(X).convert_dtypes()
            for col in X.columns:
                if X[col].dtype=="string":
                    X[col]=X[col].astype('object')

        #get column info to detect categorical columns
        data_info=get_data_info(X)
        self.categorical_ix = [c["id"] for c in data_info["categorical_columns"]]
        self.numerical_ix=[c["id"] for c in data_info["numerical_columns"]]
        #create and fit category encoder
        self.encoder = ce.OrdinalEncoder(X, handle_missing="return_nan")
        X=self.encoder.fit_transform(X)


        #create a mixed datatype distance measure
        if self.distance=='heom':
            distance_metric = HEOM(X, cat_ix=self.categorical_ix, encode_categories=False, nan_equivalents = [12345]).get_distance
        elif self.distance=='hvdm':
            bins = numpy.linspace(min(y), max(y), 20)
            d_y = numpy.digitize(y, bins)
            distance_metric = HVDM(X, d_y, cat_ix=self.categorical_ix).get_distance
        elif self.distance=='vdm':
            distance_metric = HEOM(X, cat_ix=self.categorical_ix, encode_categories=False).get_distance
        else:
            raise Exception("Unknow distance measure. Expected 'heom', 'hvdm' or 'vdm' got :"+ self.distance)
        if not isinstance(X, numpy.ndarray):
            if hasattr(X, 'values'):
                X = X.values
        if not isinstance(X, numpy.ndarray):
            raise TypeError("'X' must be an array.")

        self.neigberhood.metric=distance_metric

        self.neigberhood.fit(X)


        self._fit_y=numpy.array(y)
        self._feature_importance=self._get_feature_importance(X, y)
        return self


    def _get_feature_importance(self, X, y):
        self.estimator.fit(X, y)
        feature_importance=self.estimator.feature_importances_
        return numpy.argsort(-feature_importance)
    def _fit_perpendicular(self, X, y, sample_weight):
        "Implements the perpendicular strategy."
        raise NotImplementedError()  # pragma: no cover

    def predict(self, X):
        """
        Runs the predictions.
        """
        X=self.encoder.transform(X)


        return [self._predict_one([x])[0] for x in tqdm(X.values)]

    def _predict_one(self, X):

        indexes=range(X[0].shape[0])

        for i in numpy.argwhere(pd.isnull(X[0])):
            indexes[i]=numpy.nan
            X[i]=12345

        result = self.neigberhood.kneighbors(X)
        local_data_x=self.neigberhood._fit_X[result[1][0]][:,self._feature_importance[:3]]
        local_data_y=self._fit_y[result[1][0]]
        estimator=clone(self.estimator)

        if self.weight_by_distance:
            estimator.fit(local_data_x, local_data_y, result[0][0])
        else:
            try:
                estimator.fit(local_data_x, local_data_y)
            except Exception as e:
                print(e)
                return [numpy.average(local_data_y)]
        pred= estimator.predict([X[0][self._feature_importance[:3]]])
        if pred[0]<0:
            pred[0]=min(self._fit_y[result[1][0]])
        if pred[0]> max(self._fit_y):
            pred[0]=max(self._fit_y)
        return pred
    def decision_function(self, X):
        """
        Calls *decision_function*.
        """
        raise NotImplementedError(  # pragma: no cover
            "Decision function is not available for this model.")


if __name__ == '__main__':
    # Example code of how the HEOM metric can be used together with Scikit-Learn
    import numpy as np


    columns_to_remove = ["isThere_SST", "isThere_TRP", "CA realise", "Annee", "Numdo"]
    # Load the dataset from sklearn
    data_origin = pd.read_excel("/Users/mohamedmentis/Downloads/TrainingData_CoutPI_et_CA_082022.xlsx")

    data=data_origin.drop(columns=columns_to_remove)

    lr=LazyRegression(weight_by_distance=True)
    target=data["PRR_PI"]

    lr.fit(data.drop(columns=["PRR_PI"]), target)
    test_data=pd.read_excel("/Users/mohamedmentis/Downloads/PI MALE 24012023.xlsx").drop(columns=columns_to_remove, errors='ignore')

    print(lr.predict(test_data.drop(columns=["PRR_PI"])))