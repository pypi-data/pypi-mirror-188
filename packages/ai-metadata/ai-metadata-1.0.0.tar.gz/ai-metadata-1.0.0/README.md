# AI-Metadata

_AI-Metadata_ is a helper library to detect and extract metadata about AI/ML models for deployment and visualization.

## Features
It's critical that an inference system needs to know their metadata information of each deployed model when it serves many AI/ML models.
For a single model, its model type, runtime, serialization method, inputs and outputs schema, and other informative fields for visualization, like model metrics, training optimization params, and so on. 

AI-metadata provides a unified API to detect and extract metadata automatically, it supports the following models by default, and more types will be added to the list.
* Scikit-learn
* XGBoost
* LightGBM
* Keras and Tensorflow(tf.keras)
* Pytorch
* PySpark
* PMML
* ONNX
* Custom

## Prerequisites
 - Python 2.7 or >= 3.5

## Dependencies
  - numpy
  - pandas
  - scikit-learn
  - pypmml
  - onnxruntime

## Installation

```bash
pip install pypmml
```

Or install the latest version from github:

```bash
pip install --upgrade git+https://github.com/autodeployai/ai-metadata.git
```

## Usage
Wrap the built model by the static method `wrap` of [`MetadataModel`](ai_metadata/base.py) with several optional arguments.
```python
from ai_metadata import MetadataModel

MetadataModel.wrap(model,
                   mining_function: 'MiningFunction' = None,
                   x_test=None,
                   y_test=None,
                   data_test=None,
                   source_object=None,
                   **kwargs)
```

### Data preparation for the following examples except of Spark:
```python
from sklearn import datasets
from sklearn.model_selection import train_test_split

X, y = datasets.load_iris(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y)
```

### 1. Example: scikit learn model
```python
from sklearn.svm import SVC

# Train a SVC model
svc = SVC(probability=True)
svc.fit(X_train, y_train)

# Wrap the model with test datasets
model = MetadataModel.wrap(svc,
                           x_test=X_test,
                           y_test=y_test)
model_metadata = model.model_metadata(as_json=True, indent=2)
```

Model metadata example of the SVC model in json:
```json
{
  "runtime": "Python3.10",
  "type": "scikit-learn",
  "framework": "Scikit-learn",
  "framework_version": "1.1",
  "function_name": "classification",
  "serialization": "joblib",
  "algorithm": "SVC",
  "metrics": {
    "accuracy": 0.9736842105263158
  },
  "inputs": [
    {
      "name": "sepal length (cm)",
      "sample": 5.0,
      "type": "float64"
    },
    {
      "name": "sepal width (cm)",
      "sample": 3.2,
      "type": "float64"
    },
    {
      "name": "petal length (cm)",
      "sample": 1.2,
      "type": "float64"
    },
    {
      "name": "petal width (cm)",
      "sample": 0.2,
      "type": "float64"
    }
  ],
  "targets": [
    {
      "name": "target",
      "sample": 0,
      "type": "int64"
    }
  ],
  "outputs": [],
  "object_source": null,
  "object_name": null,
  "params": {
    "C": "1.0",
    "break_ties": "False",
    "cache_size": "200",
    "class_weight": "None",
    "coef0": "0.0",
    "decision_function_shape": "ovr",
    "degree": "3",
    "gamma": "scale",
    "kernel": "rbf",
    "max_iter": "-1",
    "probability": "True",
    "random_state": "None",
    "shrinking": "True",
    "tol": "0.001",
    "verbose": "False"
  }
}
```

### 2. Example: PMML model
```python
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from nyoka import skl_to_pmml # Export the pipeline of scikit-learn to PMML

# Train a pipeline 
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", DecisionTreeClassifier())
])
pipeline.fit(X_train, y_train)

# Export to PMML
pmml_model = './pmml-cls.xml'
skl_to_pmml(pipeline, X_train.columns, y_train.name, pmml_model)

# Wrap the model with test datasets
model = MetadataModel.wrap(pmml_model,
                           x_test=X_test,
                           y_test=y_test)
model_metadata = model.model_metadata(as_json=True, indent=2)
```

Model metadata example of the PMML model in json:
```json
{
  "runtime": "PyPMML",
  "type": "pmml",
  "framework": "PMML",
  "framework_version": "4.4.1",
  "function_name": "classification",
  "serialization": "pmml",
  "algorithm": "TreeModel",
  "metrics": {
    "accuracy": 0.9736842105263158
  },
  "inputs": [
    {
      "name": "sepal length (cm)",
      "sample": 5.0,
      "type": "double"
    },
    {
      "name": "sepal width (cm)",
      "sample": 3.2,
      "type": "double"
    },
    {
      "name": "petal length (cm)",
      "sample": 1.2,
      "type": "double"
    },
    {
      "name": "petal width (cm)",
      "sample": 0.2,
      "type": "double"
    }
  ],
  "targets": [
    {
      "name": "target",
      "sample": 0,
      "type": "integer"
    }
  ],
  "outputs": [
    {
      "name": "probability_0",
      "type": "double"
    },
    {
      "name": "probability_1",
      "type": "double"
    },
    {
      "name": "probability_2",
      "type": "double"
    },
    {
      "name": "predicted_target",
      "type": "integer"
    }
  ],
  "object_source": null,
  "object_name": null,
  "params": {}
}
```

### 3. Example: ONNX model
```python
from sklearn.linear_model import LogisticRegression
import onnxmltools # Export to ONNX
from onnxmltools.convert.common.data_types import FloatTensorType

# Train a Logistic Regression model
clf = LogisticRegression()
clf.fit(X_train, y_train)

# Export to ONNX
initial_types = [('X', FloatTensorType([None, X_test.shape[1]]))]
onnx_model = onnxmltools.convert_sklearn(clf, initial_types=initial_types)

# Wrap the model with test datasets
model = MetadataModel.wrap(onnx_model,
                           x_test=X_test,
                           y_test=y_test)
model_metadata = model.model_metadata(as_json=True, indent=2)
```

Model metadata example of the ONNX model in json:
```json
{
  "runtime": "ONNXRuntime",
  "type": "onnx",
  "framework": "ONNX",
  "framework_version": "8",
  "function_name": "classification",
  "serialization": "onnx",
  "algorithm": "LinearClassifier",
  "metrics": {
    "accuracy": 1.0
  },
  "inputs": [
    {
      "name": "X",
      "type": "tensor(float)",
      "shape": [
        null,
        4
      ],
      "sample": [
        [
          5.0,
          3.2,
          1.2,
          0.2
        ]
      ]
    }
  ],
  "targets": [],
  "outputs": [
    {
      "name": "output_label",
      "type": "tensor(int64)",
      "shape": [
        null
      ]
    },
    {
      "name": "output_probability",
      "type": "seq(map(int64,tensor(float)))",
      "shape": []
    }
  ],
  "object_source": null,
  "object_name": null,
  "params": {}
}
```

### 4. Example: Spark MLlib model
```python
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline

# Convert pandas dataframe to the dataframe of Spark
spark = SparkSession.builder.getOrCreate()
iris = datasets.load_iris(as_frame=True)
df = spark.createDataFrame(iris.frame)
df_train, df_test = df.randomSplit([0.75, 0.25])

# Train a pipeline of Spark
assembler = VectorAssembler(inputCols=iris.feature_names,
                            outputCol='features')
lr = LogisticRegression().setLabelCol(iris.target.name)
pipeline = Pipeline(stages=[assembler, lr])
pipeline_model = pipeline.fit(df_train)

# Wrap the model with test dataset
model = MetadataModel.wrap(pipeline_model,
                           data_test=df_test)
model_metadata = model.model_metadata(as_json=True, indent=2)
```

Model metadata example of the Spark model in json:
```json
{
  "runtime": "Python3.10",
  "type": "mllib",
  "framework": "Spark",
  "framework_version": "3.3",
  "function_name": "classification",
  "serialization": "spark",
  "algorithm": "PipelineModel",
  "metrics": {
    "accuracy": 0.8780487804878049
  },
  "inputs": [
    {
      "name": "sepal length (cm)",
      "sample": 4.8,
      "type": "float"
    },
    {
      "name": "sepal width (cm)",
      "sample": 3.4,
      "type": "float"
    },
    {
      "name": "petal length (cm)",
      "sample": 1.6,
      "type": "float"
    },
    {
      "name": "petal width (cm)",
      "sample": 0.2,
      "type": "float"
    }
  ],
  "targets": [
    {
      "name": "target",
      "sample": 0.0,
      "type": "float"
    }
  ],
  "outputs": [],
  "object_source": null,
  "object_name": null,
  "params": {
    "VectorAssembler_43c37a968944": {
      "outputCol": "features",
      "handleInvalid": "error",
      "inputCols": [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)"
      ]
    },
    "LogisticRegression_98944bb4d096": {
      "aggregationDepth": 2,
      "elasticNetParam": 0.0,
      "family": "auto",
      "featuresCol": "features",
      "fitIntercept": true,
      "labelCol": "target",
      "maxBlockSizeInMB": 0.0,
      "maxIter": 100,
      "predictionCol": "prediction",
      "probabilityCol": "probability",
      "rawPredictionCol": "rawPrediction",
      "regParam": 0.0,
      "standardization": true,
      "threshold": 0.5,
      "tol": 1e-06
    }
  }
}
```


You can refer to the tests of different model types for more details.


## Support
If you have any questions about the _AI-Metadata_ library, please open issues on this repository.

## License
_AI-metadata_ is licensed under [APL 2.0](http://www.apache.org/licenses/LICENSE-2.0).

