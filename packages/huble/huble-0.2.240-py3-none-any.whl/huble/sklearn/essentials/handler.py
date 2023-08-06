class EssentialsHandler:

    def __init__(self) -> None:
        pass
        
    def return_function(self, function_name: str,params:dict):
        essentials = {
            "Train-Test Split": self.__train_test_split,
            "Train Model": self.__train_model,
        }
        return essentials[function_name](params)
 
    def __train_test_split(self, params):
        parameters = {
            "test_size": params["test_size"],
        }
        return f"training_dataset, test_dataset = huble.sklearn.train_test_split(data=data,parameters={parameters})"


    def __train_model(self, params):
        return f"Model = huble.sklearn.train_model(data=training_dataset, model=model, column='{params['target_column']}')"

