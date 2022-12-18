

from aelf_sdk import rsu_contract_pb2 as contract
from aelf_sdk.types_pb2 import Address
from aelf_sdk import AElf
from google.protobuf.wrappers_pb2 import StringValue, Int64Value
from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp
import pbjson
import base58
from datetime import datetime
from protobuf_to_dict import protobuf_to_dict


class bc_plugin:
    def __init__(self, priKey, ip) -> None:
        self.aelfChain = AElf('http://'+ip)
        self._priKey = priKey
        self.contractAddress = str(
            "2LUmicHyH4RXrMjG4beDwuDsiWJESyLkgkwPdGTR8kahRzq5XS")

    def getTransactionResult(self, input):
        ret = self.aelfChain.get_transaction_result(input)

        formattedRet = dict()
        return ret

    def transConstructor(self, input, function):
        transaction = self.aelfChain.create_transaction(
            self.contractAddress,
            function,
            input.SerializeToString()
        )
        transaction = self.aelfChain.sign_transaction(
            self._priKey, transaction)
        return transaction

    def Initialize(self, input):
        transInput = contract.InitializeInput()

        transInput.Info.Addr.value = base58.b58decode_check(
            input["BasicInfo"]["Addr"])
        transInput.Info.RegTime.FromDatetime(datetime.strptime(
            input["BasicInfo"]["RegTime"], "%Y-%m-%d %H:%M:%S"))
        transInput.Info.ServerSign = input["BasicInfo"]["ServerSign"]

        for addr in input["AdjInfo"]:
            node = transInput.AdjInfo.Nodes.add()
            node.value = base58.b58decode_check(addr[0])

        transaction = self.transConstructor(transInput, "Initialize")
        result = self.aelfChain.send_transaction(
            transaction.SerializePartialToString().hex())

        print(result['TransactionId'])
        return result['TransactionId']

    def UploadPositiveCheckResult(self):
        pass

    def UploadCloudCheckResult(self):
        pass

    def DeclareNodeCheck(self, input):
        transInput = StringValue()
        transInput.value = input

        transaction = self.transConstructor(transInput, "DeclareNodeCheck")
        result = self.aelfChain.send_transaction(
            transaction.SerializePartialToString().hex())

        print("DeclareNodeCheck: " + str(result['TransactionId']))
        return result['TransactionId']

    def ReciteNode(self, input):
        transInput = contract.ReciteInput()
        transInput.To.value = base58.b58decode_check(input["To"])
        transInput.Result = input["Result"]
        transInput.Round = input["Round"]

        transaction = self.transConstructor(transInput, "ReciteNode")
        result = self.aelfChain.send_transaction(
            transaction.SerializePartialToString().hex())

        print(result['TransactionId'])
        return result['TransactionId']

    def GetCheckResult(self, round) -> dict:
        transInput = Int64Value()
        transInput.value = round
        transaction = self.transConstructor(transInput, "GetCheckResult")
        result = self.aelfChain.execute_transaction(transaction)
        print(result)
        ret = contract.RoundResult()
        ret.ParseFromString(bytes.fromhex(result.decode()))
        formattedRet = protobuf_to_dict(ret)

        return formattedRet

    def GetStatus(self):
        pass
    
    def UpdateLongTermCache(self, input):
        transInput = contract.LongTermCacheInput()
        transInput.DataHash = input
        
        transaction = self.transConstructor(transInput, "UpdateLongTermCache")
        result = self.aelfChain.send_transaction(
            transaction.SerializePartialToString().hex())

        print(result['TransactionId'])
        return result['TransactionId']
    
    def getDataHash(self, input):
        transInput = Int64Value()
        transInput.value = input
        
        transaction = self.transConstructor(transInput, "GetDataHash")
        
        result = self.aelfChain.execute_transaction(transaction)
        ret = StringValue()
        ret.ParseFromString(bytes.fromhex(result.decode()))
        formattedRet = protobuf_to_dict(ret)

        return formattedRet
