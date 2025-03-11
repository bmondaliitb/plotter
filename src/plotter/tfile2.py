from ROOT import TFile
import ROOT

class TFile2:
    """Enhanced TFile wrapper for ROOT 6.32 compatibility.
    Provides context management and directory handling.
    """

    def __init__(self, filename, option="READ"):
        self.file = ROOT.TFile.Open(filename, option)
        if not self.file or self.file.IsZombie():
            raise RuntimeError(f"Failed to open ROOT file: {filename}")

    def IsZombie(self):
        """Check if the file is a zombie."""
        return self.file.IsZombie()

    def mkdir_and_cd(self, dirName: str):
        """Creates a directory and enters it."""
        return _MkdirContext(self.file, dirName)

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file and self.file.IsOpen():
            self.file.Close()

    def Get(self, name):
        """Get object by name."""
        return self.file.Get(name)

class _MkdirContext:
    """Context manager for TFile.mkdir handling."""

    def __init__(self, tFile: ROOT.TFile, dirName: str):
        self.tFile = tFile
        self.dirName = dirName
        self._dir = self.tFile.GetDirectory(self.dirName)
        if not self._dir:
            self.tFile.mkdir(self.dirName)
            self._dir = self.tFile.GetDirectory(self.dirName)

    def __enter__(self):
        self.tFile.cd(self.dirName)
        return self._dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tFile.cd()
