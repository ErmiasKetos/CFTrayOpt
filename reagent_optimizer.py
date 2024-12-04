from collections import defaultdict
from itertools import permutations, combinations

class ReagentOptimizer:
    def __init__(self):
        self.experiment_data = {
            1: {"name": "Copper (II) (LR)", "reagents": [{"code": "KR1E", "vol": 850}, {"code": "KR1S", "vol": 300}]},
            2: {"name": "Lead (II) Cadmium (II)", "reagents": [{"code": "KR1E", "vol": 850}, {"code": "KR2S", "vol": 400}]},
            3: {"name": "Arsenic (III)", "reagents": [{"code": "KR3E", "vol": 850}, {"code": "KR3S", "vol": 400}]},
            4: {"name": "Nitrates-N (LR)", "reagents": [{"code": "KR4E", "vol": 850}, {"code": "KR4S", "vol": 300}]},
            5: {"name": "Chromium (VI) (LR)", "reagents": [{"code": "KR5E", "vol": 500}, {"code": "KR5S", "vol": 400}]},
            6: {"name": "Manganese (II) (LR)", "reagents": [{"code": "KR6E1", "vol": 500}, {"code": "KR6E2", "vol": 500}, {"code": "KR6E3", "vol": 300}]},
            7: {"name": "Boron (Dissolved)", "reagents": [{"code": "KR7E1", "vol": 1100}, {"code": "KR7E2", "vol": 1860}]},
            8: {"name": "Silica (Dissolved)", "reagents": [{"code": "KR8E1", "vol": 500}, {"code": "KR8E2", "vol": 1600}]},
            9: {"name": "Free Chlorine", "reagents": [{"code": "KR9E1", "vol": 1000}, {"code": "KR9E2", "vol": 1000}]},
            10: {"name": "Total Hardness", "reagents": [{"code": "KR10E1", "vol": 2000}, {"code": "KR10E2", "vol": 2000}, {"code": "KR10E3", "vol": 1600}]},
            11: {"name": "Total Alkalinity (LR)", "reagents": [{"code": "KR11E", "vol": 2000}]},
            12: {"name": "Orthophosphates-P (LR)", "reagents": [{"code": "KR12E1", "vol": 500}, {"code": "KR12E2", "vol": 500}, {"code": "KR12E3", "vol": 200}]},
            13: {"name": "Mercury (II)", "reagents": [{"code": "KR13E1", "vol": 850}, {"code": "KR13S", "vol": 300}]},
            14: {"name": "Selenium (IV)", "reagents": [{"code": "KR14E", "vol": 500}, {"code": "KR14S", "vol": 300}]},
            15: {"name": "Zinc (II) (LR)", "reagents": [{"code": "KR15E", "vol": 850}, {"code": "KR15S", "vol": 400}]},
            16: {"name": "Iron (Dissolved)", "reagents": [{"code": "KR16E1", "vol": 1000}, {"code": "KR16E2", "vol": 1000}, {"code": "KR16E3", "vol": 1000}, {"code": "KR16E4", "vol": 1000}]},
            17: {"name": "Residual Chlorine", "reagents": [{"code": "KR17E1", "vol": 1000}, {"code": "KR17E2", "vol": 1000}]},
            18: {"name": "Zinc (HR)", "reagents": [{"code": "KR18E1", "vol": 1000}, {"code": "KR18E2", "vol": 1000}]},
            19: {"name": "Manganese  (HR)", "reagents": [{"code": "KR19E1", "vol": 1000}, {"code": "KR19E2", "vol": 1000}, {"code": "KR19E3", "vol": 1000}]},
            20: {"name": "Orthophosphates-P (HR) ", "reagents": [{"code": "KR20E", "vol": 1600}]},
            21: {"name": "Total Alkalinity (HR)", "reagents": [{"code": "KR21E1", "vol": 2000}]},
            22: {"name": "Fluoride", "reagents": [{"code": "KR22E1", "vol": 1000},{"code": "KR22E2", "vol": 1000}]},
            27: {"name": "Molybdenum", "reagents": [{"code": "KR27E1", "vol": 1000}, {"code": "KR27E2", "vol": 1000}]},
            28: {"name": "Nitrates-N (HR)", "reagents": [{"code": "KR28E1", "vol": 1000}, {"code": "KR28E2", "vol": 2000}, {"code": "KR28E3", "vol": 2000}]},
            29: {"name": "Total Ammonia-N", "reagents": [{"code": "KR29E1", "vol": 850}, {"code": "KR29E2", "vol": 850}, {"code": "KR29E3", "vol": 850}]},
            30: {"name": "Chromium (HR)", "reagents": [{"code": "KR30E1", "vol": 1000},{"code": "KR30E2", "vol": 1000}, {"code": "KR30E3", "vol": 1000}]},
            31: {"name": "Nitrite-N", "reagents": [{"code": "KR31E1", "vol": 1000}, {"code": "KR31E2", "vol": 1000}]},
            34: {"name": "Nickel (HR)", "reagents": [{"code": "KR34E1", "vol": 500}, {"code": "KR34E2", "vol": 500}]},
            35: {"name": "Copper (II) (HR)", "reagents": [{"code": "KR35E1", "vol": 1000}, {"code": "KR35E2", "vol": 1000}]},
            36: {"name": "Sulfate", "reagents": [{"code": "KR36E1", "vol": 1000}, {"code": "KR36E2", "vol": 2300}]},
            40: {"name": "Potassium", "reagents": [{"code": "KR40E1", "vol": 2000}, {"code": "KR40E2", "vol": 1000}]},
            42: {"name": "Aluminum-BB", "reagents": [{"code": "KR42E1", "vol": 1000}, {"code": "KR42E2", "vol": 1000}]}
        }
        self.MAX_LOCATIONS = 16

    def calculate_tests(self, volume_ul, capacity_ml):
        """Calculate number of tests possible for a given volume and capacity"""
        return int((capacity_ml * 1000) / volume_ul)

    def get_location_capacity(self, location):
        """Get the capacity of a location in mL"""
        return 270 if location < 4 else 140

    def _generate_possible_assignments(self, selected_experiments):
        """Generate all possible reagent assignments"""
        assignments = []
        for exp_num in selected_experiments:
            exp_data = self.experiment_data[exp_num]
            for i, reagent in enumerate(exp_data["reagents"]):
                assignments.append((exp_num, i, reagent["vol"]))
        return assignments

    def _calculate_configuration_days(self, assignment_map, daily_counts):
        """Calculate days of operation for a given configuration"""
        experiment_tests = defaultdict(lambda: defaultdict(int))
        
        # Calculate tests possible for each reagent
        for loc, (exp_num, reagent_idx, _) in assignment_map.items():
            reagent = self.experiment_data[exp_num]["reagents"][reagent_idx]
            capacity = self.get_location_capacity(loc)
            tests = self.calculate_tests(reagent["vol"], capacity)
            experiment_tests[exp_num][reagent["code"]] += tests

        # Calculate days for each experiment
        days_by_exp = {}
        for exp_num in daily_counts.keys():
            if exp_num in experiment_tests:
                min_tests = min(experiment_tests[exp_num].values())
                days = min_tests / daily_counts[exp_num]
                days_by_exp[exp_num] = days
            else:
                days_by_exp[exp_num] = 0

        return min(days_by_exp.values()) if days_by_exp else 0

    def _create_configuration(self, assignment_map, daily_counts):
        """Create full configuration from assignment map"""
        config = {
            "tray_locations": [None] * self.MAX_LOCATIONS,
            "results": {},
            "daily_counts": daily_counts
        }

        experiment_tests = defaultdict(lambda: defaultdict(int))
        
        # Create tray_locations and calculate tests
        for loc, (exp_num, reagent_idx, _) in assignment_map.items():
            reagent = self.experiment_data[exp_num]["reagents"][reagent_idx]
            capacity = self.get_location_capacity(loc)
            tests = self.calculate_tests(reagent["vol"], capacity)
            
            config["tray_locations"][loc] = {
                "reagent_code": reagent["code"],
                "experiment": exp_num,
                "tests_possible": tests,
                "volume_per_test": reagent["vol"],
                "capacity": capacity
            }
            
            experiment_tests[exp_num][reagent["code"]] += tests

        # Calculate results for each experiment
        for exp_num in daily_counts.keys():
            if exp_num in experiment_tests:
                min_tests = min(experiment_tests[exp_num].values())
                days = min_tests / daily_counts[exp_num]
                
                config["results"][exp_num] = {
                    "name": self.experiment_data[exp_num]["name"],
                    "total_tests": min_tests,
                    "daily_count": daily_counts[exp_num],
                    "days_of_operation": days
                }

        # Calculate overall days of operation
        config["overall_days_of_operation"] = min(
            result["days_of_operation"] 
            for result in config["results"].values()
        )

        return config

    def optimize_tray_configuration(self, selected_experiments, daily_counts):
        """Optimize tray configuration for maximum days of operation"""
        # Validate inputs
        for exp in selected_experiments:
            if exp not in self.experiment_data:
                raise ValueError(f"Invalid experiment number: {exp}")
            if exp not in daily_counts or daily_counts[exp] <= 0:
                raise ValueError(f"Invalid daily count for experiment {exp}")

        # Generate possible assignments
        assignments = self._generate_possible_assignments(selected_experiments)
        
        # Calculate total locations needed
        total_locations_needed = sum(len(self.experiment_data[exp]["reagents"]) 
                                   for exp in selected_experiments)
        
        if total_locations_needed > self.MAX_LOCATIONS:
            raise ValueError(f"Selected experiments require {total_locations_needed} locations, "
                           f"exceeding maximum of {self.MAX_LOCATIONS}")

        best_days = 0
        best_assignment = None
        
        # Try different location assignments
        for perm in permutations(range(self.MAX_LOCATIONS), len(assignments)):
            assignment_map = {loc: assignment for loc, assignment in zip(perm, assignments)}
            days = self._calculate_configuration_days(assignment_map, daily_counts)
            
            if days > best_days:
                best_days = days
                best_assignment = assignment_map

        if best_assignment:
            return self._create_configuration(best_assignment, daily_counts)
        else:
            raise ValueError("Could not find valid configuration")

    def get_available_experiments(self):
        """Return list of available experiments"""
        return [{"id": id_, "name": exp["name"]} 
                for id_, exp in self.experiment_data.items()]

    def get_reagent_info(self, reagent_code):
        """Get information about a specific reagent code"""
        for exp_id, exp_data in self.experiment_data.items():
            for reagent in exp_data["reagents"]:
                if reagent["code"] == reagent_code:
                    return {
                        "experiment_id": exp_id,
                        "experiment_name": exp_data["name"],
                        "volume": reagent["vol"]
                    }
        return None

    def get_location_info(self, location):
        """Get capacity and other information about a specific location"""
        return {
            "location_number": location + 1,
            "capacity": self.get_location_capacity(location),
            "is_high_capacity": location < 4
        }
        
    def validate_configuration(self, config):
        """Validate a configuration for correctness"""
        # Check all locations are properly assigned
        if any(loc is None for loc in config["tray_locations"]):
            return False
            
        # Verify each experiment has all necessary reagents
        for exp_num in config["results"]:
            reagent_counts = defaultdict(int)
            required_reagents = {r["code"] for r in self.experiment_data[exp_num]["reagents"]}
            
            for loc in config["tray_locations"]:
                if loc["experiment"] == exp_num:
                    reagent_counts[loc["reagent_code"]] += 1
            
            if not all(reagent_counts[r] > 0 for r in required_reagents):
                return False
        
        return True

    def get_experiment_summary(self, exp_num, config):
        """Get detailed summary for an experiment in the configuration"""
        if exp_num not in config["results"]:
            return None
            
        result = config["results"][exp_num]
        reagent_locations = defaultdict(list)
        
        for i, loc in enumerate(config["tray_locations"]):
            if loc and loc["experiment"] == exp_num:
                reagent_locations[loc["reagent_code"]].append({
                    "location": i,
                    "tests": loc["tests_possible"],
                    "capacity": loc["capacity"]
                })
                
        return {
            "name": result["name"],
            "total_tests": result["total_tests"],
            "daily_count": result["daily_count"],
            "days_of_operation": result["days_of_operation"],
            "reagent_locations": dict(reagent_locations)
        }

    def calculate_efficiency(self, config):
        """Calculate efficiency metrics for the configuration"""
        total_capacity = sum(self.get_location_capacity(i) for i in range(self.MAX_LOCATIONS))
        used_capacity = sum(loc["capacity"] for loc in config["tray_locations"] if loc)
        
        return {
            "capacity_utilization": used_capacity / total_capacity,
            "days_of_operation": config["overall_days_of_operation"],
            "total_experiments": len(config["results"]),
            "high_capacity_slots_used": sum(1 for i, loc in enumerate(config["tray_locations"]) 
                                          if loc and i < 4)
        }

    def export_configuration(self, config):
        """Export configuration in a structured format"""
        return {
            "configuration_summary": {
                "total_experiments": len(config["results"]),
                "overall_days": config["overall_days_of_operation"],
                "daily_counts": config["daily_counts"]
            },
            "locations": [
                {
                    "location": i,
                    "capacity": self.get_location_capacity(i),
                    "reagent": loc["reagent_code"] if loc else None,
                    "experiment": loc["experiment"] if loc else None,
                    "tests_possible": loc["tests_possible"] if loc else 0
                }
                for i, loc in enumerate(config["tray_locations"])
            ],
            "experiments": [
                {
                    "experiment_id": exp_id,
                    "name": result["name"],
                    "total_tests": result["total_tests"],
                    "daily_count": result["daily_count"],
                    "days_of_operation": result["days_of_operation"]
                }
                for exp_id, result in config["results"].items()
            ]
        }
