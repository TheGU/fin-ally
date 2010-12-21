class ExpenseTypeThread():
    """This class supports global ExpenseType updates. It will execute every function
    present in the class variable refreshFuncList when the method RunRefreshFuncs is
    called. This class is intended to provide unified updates for all expenseType
    components when any modification to the underlying expenseType objects are made."""
    
    refreshFuncList = []
    
    def StoreRefreshFunc(self, func):
        self.__class__.refreshFuncList.append(func)
        
    def ClearRefreshFuncList(self):
        self.__class__.refreshFuncList = []
        
    def RunRefreshFuncs(self):
        for i in self.__class__.refreshFuncList:
            i() # actually execute the function