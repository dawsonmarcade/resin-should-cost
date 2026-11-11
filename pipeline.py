"""
Run every stage in order:
    py -m src.pipeline
 
Each stage can also be run on its own (py -m src.load, src.transform, src.model).
"""
from src import load, model, transform
 
 
def main():
    print("[1/3] load")
    load.main()
    print("\n[2/3] transform")
    transform.main()
    print("\n[3/3] model")
    model.main()
 
 
if __name__ == "__main__":
    main()