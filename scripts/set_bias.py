from fenja_health_dl.model import MODEL

print("MODEL LOADED:", MODEL)
print("BIAS BEFORE:", MODEL.bias)

MODEL.bias = 0.1
MODEL.save()

print("SAVED")
