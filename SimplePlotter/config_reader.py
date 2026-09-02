import yaml  # Assuming the config file is in YAML format

class ConfigReader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.job = None
        self.samples = []
        self.plots = []

    def read_config(self):
        """Read the configuration file and store the data."""
        with open(self.config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            # apply common styles to all samples
            common_styles = config_data["Job"].get("CommonStyles", {})
            for plot in config_data.get("Plot", []):
                for sample in plot.get("samples", []):
                    for k, v in common_styles.items():
                        sample.setdefault(k, v)

        # Store the Job block
        self.job = config_data.get("Job", {})

        # Store the Sample block
        self.samples = config_data.get("Sample", [])

        # Store the Plot block
        self.plots = config_data.get("Plot", [])

    def get_job(self):
        """Return the Job configuration."""
        return self.job

    def get_samples(self):
        """Return the list of samples."""
        return self.samples

    def get_plots(self):
        """Return the list of plots."""
        return self.plots

    def print_config(self):
        """Print the configuration data."""
        print("Job Configuration:")
        print(self.job)
        print("\nSample Configuration:")
        for sample in self.samples:
            print(sample)
        print("\nPlot Configuration:")
        for plot in self.plots:
            print(plot)