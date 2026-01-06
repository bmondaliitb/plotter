import ROOT                                                 
                                                                                                                             
class RootFile:                                                                                                            
    """Thin ROOT file wrapper with context-manager support."""                          
    def __init__(self, path, option="READ"):                
        self._file = ROOT.TFile.Open(path, option)                                                                         
        if not self._file or self._file.IsZombie():                                                                        
            raise RuntimeError(f"Failed to open ROOT file: {path}")                                                        
                                                                                                                           
    def Get(self, name):                                    
        return self._file.Get(name)                                                                                        
                                                                                                                           
    def IsZombie(self):                                                                                                    
        return self._file.IsZombie()                        
                                                            
    def Close(self):                                        
        if self._file and self._file.IsOpen():                                                                             
            self._file.Close()                                                                                             
                                                                                                                           
    def __enter__(self):                                    
        return self._file                                                                                                  
                                                            
    def __exit__(self, exc_type, exc_val, exc_tb):          
        self.Close()