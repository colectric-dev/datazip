from io import BytesIO

from datazip import DataZip

if __name__ == "__main__":
    with DataZip(temp := BytesIO(), "w") as dz:
        dz["five"] = 5
        assert dz["five"] == 5
