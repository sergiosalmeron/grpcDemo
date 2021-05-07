import iris_pb2 as irisProto
import iris_pb2_grpc as irisProtoGRPC

from sklearn import datasets
from sklearn.svm import SVC

import grpc
import concurrent.futures

import logging, os, json, time


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def generateModel():
    iris = datasets.load_iris()
    clf = SVC()
    #clf.fit(iris.data, iris.target)
    clf.fit(iris.data, iris.target_names[iris.target])
    return clf

"""
    def classify1(self, request, context):
        logging.info("Classifying: %s", request)
        prediction = self.model.predict([[request.SepalLength, request.SepalWidth, request.PetalLength, request.PetalWidth]])
        logging.info("Finished. Prediction was: " + str(prediction))
        #return getattr(irisProto, "result.IrisType."+prediction.upper())
        
        return getattr(irisProto.result.IrisType, str(result[0]).upper()) 
    """    

class GuessTypeServicer(irisProtoGRPC.GuessTypeServicer):
    def __init__(self):
        self.model = generateModel()

    def classify1(self, request, context):
        logging.info("Classifying: %s", request)
        prediction = self.model.predict([[request.SepalLength, request.SepalWidth, request.PetalLength, request.PetalWidth]])
        predictedclass = str(prediction[0]).upper()
        logging.info("Finished. Prediction was: " + predictedclass)
        logging.info("type: "+str(type(predictedclass)))
        #predictedclass = getattr(irisProto.result.IrisType, predictedclass)
        #predictedclass = irisProto.result.IrisType.VERSICOLOR
        #predictedclass = irisProto.result.IrisType.Name(predictedclass)
        logging.info("sending class: " + str(predictedclass))
        #result = irisProto.result(specie = predictedclass)
        result = irisProto.result(specie = irisProto.result.IrisType.Value(predictedclass))
        #result = irisProto.result(specie=irisProto.result.IrisType.VERSICOLOR)
        logging.info("sending : " + str(result))
        return result

    def classify2(self, request, context):        
        return irisProto.result(specie=irisProto.result.IrisType.VERSICOLOR)
    
"""configfile = os.environ['CONFIG'] if 'CONFIG' in os.environ else "config.json"
logging.info("loading config from %s", configfile)
config = json.load(open(configfile, 'rt'))
grpcport = config['grpcport']"""
grpcport = 8061
grpcserver = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
#asp_pb2_grpc.add_OneshotSolverServicer_to_server(GRPCOneshotSolverServicer(), grpcserver)
irisProtoGRPC.add_GuessTypeServicer_to_server(GuessTypeServicer(), grpcserver)

# listen on all interfaces (otherwise docker cannot export)
grpcserver.add_insecure_port('0.0.0.0:'+str(grpcport))
logging.info("starting grpc server at port %d", grpcport)
grpcserver.start()

while True:
    time.sleep(1)
        
