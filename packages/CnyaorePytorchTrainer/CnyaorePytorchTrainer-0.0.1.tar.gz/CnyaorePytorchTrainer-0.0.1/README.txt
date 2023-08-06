This is a PyTorch Model Trainer Class. It trains, validates input data.
It also saves the model after training to avoid retraining.
The class takes in 7 arguments i.e. device, epochs, model, criterion, 
                                    optimizer, trainloader, valloader.
It has 2 methods:
    1. model_train_validate()
        - This train, validate data
        - It also plots learning curves
        - Finally it saves the model to avoid retraining it
    2. load_model()
        - This loads your saved model from the above function i.e. model_train_validate()