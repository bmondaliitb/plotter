echo "activate venv ...."
DIR=/mnt/nvme0n1p4/HEP/Work/Project-W-Z/Plotter/
source $DIR/venv/bin/activate

echo "setup root"
sroot

echo "Adding SimplePlotter to PATH"
export PATH="$PATH:$DIR/plotter/SimplePlotter"

