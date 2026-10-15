"""Prepare the existing model from the author's pinned Spring_2026 archive."""
import argparse
import hashlib
import io
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "a9e209d5b305b6472572837d600d153050af8446"
SOURCE_URL = (
    "https://raw.githubusercontent.com/golovanov-andrei/Spring_2026/"
    + SOURCE_COMMIT + "/Lr2/Moscow.zip"
)
ARCHIVE_SHA256 = "23afd5acbbccce8e3da37986fbcaa9bfffe24423ff70c4af62bb33b72c29d4e1"
MODEL_SHA256 = "93bcb857b84ee1b8097c416d6edf2f02293832d6b0e4f20260f1110ce672f56e"


def prepare(archive_path=None):
    destination = ROOT / "catboost_model.cbm"
    if destination.exists():
        if hashlib.sha256(destination.read_bytes()).hexdigest() == MODEL_SHA256:
            print("Model is ready:", destination.name)
            return destination
        raise ValueError("A different model already exists; keep it or rename it before preparing the original.")
    if archive_path is None:
        with urlopen(SOURCE_URL, timeout=45) as response:
            archive = response.read(8 * 1024 * 1024 + 1)
    else:
        archive = Path(archive_path).read_bytes()
    if hashlib.sha256(archive).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Archive checksum does not match the pinned source")
    with ZipFile(io.BytesIO(archive)) as source:
        model = source.read("catboost_model.cbm")
    if hashlib.sha256(model).hexdigest() != MODEL_SHA256:
        raise ValueError("Model checksum does not match")
    temporary = destination.with_suffix(".cbm.tmp")
    temporary.write_bytes(model)
    temporary.replace(destination)
    print("Prepared original CatBoost model:", len(model), "bytes")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="Use an already downloaded Moscow.zip")
    args = parser.parse_args()
    prepare(args.archive)
