def delete_object(x):
    if x.number_of_tablets_or_ml == 0:
        return x.delete()