from cpanlp.person.consumer import *
keyword = "你好"
class Signal:
    def __init__(self, signal):
        self.signal = signal
        self.cost = 0
        self.is_high_cost = True if self.cost >20000 else False
#例如，在劳动市场中，一个人的学历可以被看作是对他的工作能力的一种信号，而他的工作能力则是信息。信号和信息之间的关系是相互依存的。信号需要信息来提供意义，而信息需要信号来传递。信号传递信息是有成本的，所以在经济学中信号传递的成本称为信息成本。        
class Information:
    def __init__(self, message):
        self.message=message
        self.signals = []
        self.value=0.0
    def extract_signal(self): 
        words = self.message.split()
        for i in range(len(words)):
            if keyword in words[i]:
                self.signals.append(" ".join(words[i:i+3]))
        return self.signals
    def send_signal(self):
        return Signal(self.signals)
class PositiveInformation(Information):
    def __init__(self, message,credibility, impact):
        super().__init__(message)
        self.credibility = credibility
        self.impact = impact

class SpeculativeInformation(Information):
    def __init__(self, message, accuracy, likelihood):
        super().__init__(message)
        self.accuracy = accuracy
        self.likelihood = likelihood

    def assess_value(self):
        return self.value * self.accuracy * self.likelihood

speculative_info = SpeculativeInformation(100, 0.7, 0.2)
class AsymmetricInformation(Information):
    def __init__(self, sender, receiver, message, hidden_information):
        super().__init__(message)
        self.sender = sender
        self.receiver = receiver
        self.hidden_information = hidden_information
    def reveal_hidden_information(self):
        print(f"{self.sender.name} reveals hidden information to {self.receiver.name}: {self.hidden_information}")
    def is_information_complete(self):
        return self.hidden_information is None
    def negotiate(self):
        if self.hidden_information is not None:
            print(f"{self.sender.name} and {self.receiver.name} are negotiating to resolve the asymmetric information problem...")
            self.hidden_information = None
            print("Asymmetric information problem resolved")
        else:
            print("No asymmetric information to resolve")
    def add_hidden_information(self, new_hidden_information):
        if self.hidden_information is None:
            self.hidden_information = new_hidden_information
        else:
            self.hidden_information += "; " + new_hidden_information
    def get_hidden_information(self):
        return self.hidden_information
    def use_information(self):
        if self.hidden_information is not None:
            print(f"{self.receiver.name} uses the information received from {self.sender.name} to make a decision")
        else:
            print("Not enough information to make a decision")
    def is_information_useful(self):
        return self.hidden_information is None
    def get_advantage(self):
        if self.hidden_information is not None:
            print(f"{self.sender.name} has an advantage over {self.receiver.name} due to asymmetric information")
        else:
            print("No advantage due to symmetric information")
            
def main():
    p1=Consumer("allen",20,1000,0)
    p2=Consumer("bob",23,30000,0)
    info = AsymmetricInformation(p1, p2, "I'm interested in buying your car", "I have a limited budget")
    info.reveal_hidden_information()
    if info.is_information_complete():
        print("Information is complete")
    else:
        print("Information is not complete")
    info.negotiate()
    info.add_hidden_information("I also have a deadline to meet")
    info.use_information()
    in1=Information("你好真不错")
    sig = in1.extract_signal()
    sig1=in1.send_signal()
    print(sig1.signal)
if __name__ == '__main__':
    main()