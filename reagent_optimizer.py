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

    def _calculate_set_tests(self, reagent_set, location_capacities):
        """Calculate possible tests for a set of reagents with given capacities"""
        tests_per_reagent = []
        for reagent, capacity in zip(reagent_set, location_capacities):
            tests = self.calculate_tests(reagent["vol"], capacity)
            tests_per_reagent.append(tests)
        return min(tests_per_reagent)

    def _evaluate_reagent_placement(self, exp_num, capacities, daily_count):
        """Evaluate how many days a specific reagent placement would provide"""
        reagents = self.experiment_data[exp_num]["reagents"]
        total_tests = self._calculate_set_tests(reagents, capacities)
        return total_tests / daily_count if daily_count > 0 else float('inf')

    
    
    def optimize_tray_configuration(self, selected_experiments, daily_counts):
        """Optimize tray configuration for maximum days of operation"""
        # Validate inputs
        for exp in selected_experiments:
            if exp not in self.experiment_data:
                raise ValueError(f"Invalid experiment number: {exp}")
            if exp not in daily_counts or daily_counts[exp] <= 0:
                raise ValueError(f"Invalid daily count for experiment {exp}")
    
        # Initialize configuration
        config = {
            "tray_locations": [None] * self.MAX_LOCATIONS,
            "results": {},
            "daily_counts": daily_counts,
            "available_locations": set(range(self.MAX_LOCATIONS))
        }
    
        # Calculate total initial reagents needed
        total_initial_reagents = sum(len(self.experiment_data[exp]["reagents"]) 
                                   for exp in selected_experiments)
        
        if total_initial_reagents > self.MAX_LOCATIONS:
            raise ValueError(f"Total reagents needed ({total_initial_reagents}) exceeds maximum locations ({self.MAX_LOCATIONS})")
    
        # First place one set of each experiment
        remaining_locations = list(config["available_locations"])
        current_location = 0
    
        for exp in selected_experiments:
            reagents = self.experiment_data[exp]["reagents"]
            num_reagents = len(reagents)
            
            # Get locations for this experiment
            exp_locations = remaining_locations[current_location:current_location + num_reagents]
            current_location += num_reagents
            
            # Place reagents
            for i, reagent in enumerate(reagents):
                loc = exp_locations[i]
                capacity = self.get_location_capacity(loc)
                tests = self.calculate_tests(reagent["vol"], capacity)
                
                config["tray_locations"][loc] = {
                    "reagent_code": reagent["code"],
                    "experiment": exp,
                    "tests_possible": tests,
                    "volume_per_test": reagent["vol"],
                    "capacity": capacity
                }
                config["available_locations"].remove(loc)
    
            # Initialize results for this experiment
            config["results"][exp] = {
                "name": self.experiment_data[exp]["name"],
                "total_tests": 0,
                "daily_count": daily_counts[exp],
                "days_of_operation": 0
            }
    
        # Fill remaining locations to maximize days of operation
        while config["available_locations"]:
            best_exp = None
            best_improvement = 0
            best_locations = None
    
            # Try each experiment in remaining locations
            for exp in selected_experiments:
                num_reagents = len(self.experiment_data[exp]["reagents"])
                if len(config["available_locations"]) >= num_reagents:
                    # Calculate current days for this experiment
                    current_tests = self._calculate_experiment_tests(config["tray_locations"], exp)
                    current_days = current_tests / daily_counts[exp]
    
                    # Try placing in available locations
                    available = sorted(list(config["available_locations"]))[:num_reagents]
                    potential_tests = self._calculate_potential_improvement(exp, available)
                    potential_days = potential_tests / daily_counts[exp]
    
                    improvement = potential_days - current_days
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_exp = exp
                        best_locations = available
    
            if best_exp and best_locations:
                # Place the best option found
                reagents = self.experiment_data[best_exp]["reagents"]
                for reagent, loc in zip(reagents, best_locations):
                    capacity = self.get_location_capacity(loc)
                    tests = self.calculate_tests(reagent["vol"], capacity)
                    
                    config["tray_locations"][loc] = {
                        "reagent_code": reagent["code"],
                        "experiment": best_exp,
                        "tests_possible": tests,
                        "volume_per_test": reagent["vol"],
                        "capacity": capacity
                    }
                    config["available_locations"].remove(loc)
            else:
                break
    
        # Calculate final results
        for exp in selected_experiments:
            total_tests = self._calculate_experiment_tests(config["tray_locations"], exp)
            days = total_tests / daily_counts[exp]
            config["results"][exp].update({
                "total_tests": total_tests,
                "days_of_operation": days
            })
    
        # Calculate overall days of operation
        config["overall_days_of_operation"] = min(
            result["days_of_operation"] for result in config["results"].values()
        )
    
        return config
        
    def _calculate_experiment_tests(self, tray_locations, exp_num):
        """Calculate total tests possible for an experiment"""
        reagent_tests = defaultdict(int)
        exp_data = self.experiment_data[exp_num]
        
        # Sum up tests possible for each reagent
        for loc in tray_locations:
            if loc and loc["experiment"] == exp_num:
                reagent_tests[loc["reagent_code"]] += loc["tests_possible"]
        
        # Return minimum tests possible across all required reagents
        if not reagent_tests:
            return 0
            
        return min(reagent_tests.values())
    
    def _calculate_potential_improvement(self, exp_num, locations):
        """Calculate potential tests if experiment is placed in given locations"""
        reagents = self.experiment_data[exp_num]["reagents"]
        tests_possible = float('inf')
        
        for reagent, loc in zip(reagents, locations):
            capacity = self.get_location_capacity(loc)
            tests = self.calculate_tests(reagent["vol"], capacity)
            tests_possible = min(tests_possible, tests)
            
        return tests_possible


    def _place_reagent_set(self, config, exp_num, locations):
        """Place a set of reagents in the specified locations"""
        exp_data = self.experiment_data[exp_num]
        reagents = sorted(exp_data["reagents"], key=lambda r: r["vol"], reverse=True)

        for loc, reagent in zip(locations, reagents):
            capacity = self.get_location_capacity(loc)
            tests = self.calculate_tests(reagent["vol"], capacity)
            
            config["tray_locations"][loc] = {
                "reagent_code": reagent["code"],
                "experiment": exp_num,
                "tests_possible": tests,
                "volume_per_test": reagent["vol"],
                "capacity": capacity
            }
            config["available_locations"].remove(loc)

    def _calculate_final_results(self, config):
        """Calculate final results for the configuration"""
        experiment_tests = defaultdict(lambda: defaultdict(int))
        
        # Calculate tests possible for each reagent
        for loc, data in enumerate(config["tray_locations"]):
            if data:
                exp_num = data["experiment"]
                experiment_tests[exp_num][data["reagent_code"]] += data["tests_possible"]

        # Calculate results for each experiment
        for exp_num, tests_data in experiment_tests.items():
            total_tests = min(tests_data.values())  # Minimum tests across all reagents
            days = total_tests / config["daily_counts"][exp_num]
            
            config["results"][exp_num] = {
                "name": self.experiment_data[exp_num]["name"],
                "total_tests": total_tests,
                "daily_count": config["daily_counts"][exp_num],
                "days_of_operation": days
            }

        # Calculate overall days of operation
        if config["results"]:
            config["overall_days_of_operation"] = min(
                result["days_of_operation"] for result in config["results"].values()
            )
        else:
            config["overall_days_of_operation"] = 0

    def get_available_experiments(self):
        """Return list of available experiments"""
        return [{"id": id_, "name": exp["name"]} 
                for id_, exp in self.experiment_data.items()]

    # Add utility methods...
    def get_reagent_info(self, reagent_code):
        """Get detailed information about a specific reagent code"""
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
        """Get information about a specific location"""
        return {
            "location_number": location + 1,
            "capacity": self.get_location_capacity(location),
            "is_high_capacity": location < 4
        }

    def get_configuration_summary(self, config):
        """Get a detailed summary of the configuration"""
        if not config:
            return None

        summary = {
            "overall_days": config["overall_days_of_operation"],
            "total_locations_used": len([loc for loc in config["tray_locations"] if loc is not None]),
            "high_capacity_usage": len([loc for i, loc in enumerate(config["tray_locations"]) 
                                      if loc is not None and i < 4]),
            "experiments": {},
            "locations": []
        }

        # Experiment details
        for exp_num, result in config["results"].items():
            exp_reagents = defaultdict(list)
            for i, loc in enumerate(config["tray_locations"]):
                if loc and loc["experiment"] == exp_num:
                    exp_reagents[loc["reagent_code"]].append({
                        "location": i + 1,
                        "tests": loc["tests_possible"],
                        "capacity": loc["capacity"]
                    })

            summary["experiments"][exp_num] = {
                "name": result["name"],
                "daily_count": result["daily_count"],
                "total_tests": result["total_tests"],
                "days_of_operation": result["days_of_operation"],
                "reagent_placements": dict(exp_reagents)
            }

        # Location details
        for i, loc in enumerate(config["tray_locations"]):
            location_info = {
                "location": i + 1,
                "capacity": self.get_location_capacity(i),
                "is_high_capacity": i < 4
            }
            if loc:
                location_info.update({
                    "reagent_code": loc["reagent_code"],
                    "experiment": loc["experiment"],
                    "tests_possible": loc["tests_possible"],
                    "volume_per_test": loc["volume_per_test"]
                })
            summary["locations"].append(location_info)

        return summary

    def validate_configuration(self, config):
        """Validate a configuration for correctness and completeness"""
        if not config or "tray_locations" not in config:
            return False

        # Check experiment completeness
        for exp_num in config.get("results", {}):
            required_reagents = {r["code"] for r in self.experiment_data[exp_num]["reagents"]}
            found_reagents = set()
            
            for loc in config["tray_locations"]:
                if loc and loc["experiment"] == exp_num:
                    found_reagents.add(loc["reagent_code"])
            
            if not required_reagents.issubset(found_reagents):
                return False

        # Validate location assignments
        for i, loc in enumerate(config["tray_locations"]):
            if loc:
                if loc["capacity"] != self.get_location_capacity(i):
                    return False
                if "tests_possible" not in loc or "volume_per_test" not in loc:
                    return False

        return True

    def calculate_optimization_metrics(self, config):
        """Calculate optimization metrics for the configuration"""
        if not config:
            return None

        total_capacity = sum(self.get_location_capacity(i) for i in range(self.MAX_LOCATIONS))
        used_capacity = sum(self.get_location_capacity(i) for i, loc in enumerate(config["tray_locations"]) if loc)

        metrics = {
            "capacity_utilization": used_capacity / total_capacity,
            "overall_days": config["overall_days_of_operation"],
            "total_locations_used": len([loc for loc in config["tray_locations"] if loc]),
            "experiments_count": len(config["results"]),
            "average_days": sum(r["days_of_operation"] for r in config["results"].values()) / len(config["results"]),
            "days_variation": max(r["days_of_operation"] for r in config["results"].values()) - 
                            min(r["days_of_operation"] for r in config["results"].values())
        }

        # Calculate efficiency by experiment
        metrics["experiment_metrics"] = {}
        for exp_num, result in config["results"].items():
            exp_locations = [i for i, loc in enumerate(config["tray_locations"]) 
                           if loc and loc["experiment"] == exp_num]
            exp_metrics = {
                "locations_used": len(exp_locations),
                "high_capacity_used": len([loc for loc in exp_locations if loc < 4]),
                "days_of_operation": result["days_of_operation"],
                "daily_efficiency": result["total_tests"] / (result["daily_count"] * len(exp_locations))
            }
            metrics["experiment_metrics"][exp_num] = exp_metrics

        return metrics

    def export_configuration(self, config, format='dict'):
        """Export the configuration in various formats"""
        if not config:
            return None

        basic_info = {
            "timestamp": datetime.now().isoformat(),
            "overall_days": config["overall_days_of_operation"],
            "total_experiments": len(config["results"]),
            "configuration": []
        }

        for i, loc in enumerate(config["tray_locations"]):
            loc_info = {
                "location": i + 1,
                "capacity": self.get_location_capacity(i)
            }
            if loc:
                loc_info.update({
                    "reagent": loc["reagent_code"],
                    "experiment": loc["experiment"],
                    "tests": loc["tests_possible"]
                })
            basic_info["configuration"].append(loc_info)

        if format == 'dict':
            return basic_info
        elif format == 'json':
            import json
            return json.dumps(basic_info, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
