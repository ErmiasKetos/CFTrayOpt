from collections import defaultdict

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
        return int((capacity_ml * 1000) / volume_ul)

    def get_location_capacity(self, location):
        return 270 if location < 4 else 140

    def optimize_tray_configuration(self, selected_experiments, daily_counts=None):
        # Initialize daily_counts if not provided
        if daily_counts is None:
            daily_counts = {exp: 1 for exp in selected_experiments}
            
        # Validate experiments and counts
        for exp in selected_experiments:
            if exp not in self.experiment_data:
                raise ValueError(f"Invalid experiment number: {exp}")
            if exp not in daily_counts or daily_counts[exp] <= 0:
                raise ValueError(f"Invalid daily count for experiment {exp}")

        # Check total reagents needed
        total_reagents = sum(len(self.experiment_data[exp]["reagents"]) for exp in selected_experiments)
        if total_reagents > self.MAX_LOCATIONS:
            details = [f"{self.experiment_data[exp]['name']}: {len(self.experiment_data[exp]['reagents'])} reagents" 
                      for exp in selected_experiments]
            raise ValueError(
                f"Total reagents needed ({total_reagents}) exceeds available locations ({self.MAX_LOCATIONS}).\n"
                f"Experiment requirements:\n" + "\n".join(details)
            )

        # Initialize configuration
        config = {
            "tray_locations": [None] * self.MAX_LOCATIONS,
            "results": {},
            "available_locations": set(range(self.MAX_LOCATIONS)),
            "daily_counts": daily_counts
        }

        # Sort experiments by complexity, volume requirements, and daily count
        sorted_experiments = sorted(
            selected_experiments,
            key=lambda x: (
                len(self.experiment_data[x]["reagents"]),
                max(r["vol"] for r in self.experiment_data[x]["reagents"]),
                -daily_counts[x],  # Prioritize experiments with higher daily counts
                -min(r["vol"] for r in self.experiment_data[x]["reagents"])
            ),
            reverse=True
        )

        # Phase 1: Place primary sets
        for exp in sorted_experiments:
            self._place_primary_set(exp, config)

        # Phase 2: Optimize additional sets
        self._optimize_additional_sets(sorted_experiments, config)

        # Calculate days of operation
        self._calculate_days_of_operation(config)

        return config

    def _place_primary_set(self, exp, config):
        exp_data = self.experiment_data[exp]
        num_reagents = len(exp_data["reagents"])
        
        # Try to place high-volume reagents in 270mL locations first
        high_volume_reagents = any(r["vol"] > 800 for r in exp_data["reagents"])
        if high_volume_reagents:
            available_270 = [loc for loc in range(4) if loc in config["available_locations"]]
            if len(available_270) >= num_reagents:
                self._place_reagent_set(exp, available_270[:num_reagents], config)
                return

        # Otherwise, find best available locations
        available_locs = sorted(config["available_locations"])
        best_locations = []
        
        # Find optimal locations based on reagent volumes
        for reagent in sorted(exp_data["reagents"], key=lambda r: r["vol"], reverse=True):
            best_loc = None
            best_efficiency = 0
            
            for loc in available_locs:
                if loc not in best_locations:
                    capacity = self.get_location_capacity(loc)
                    tests = self.calculate_tests(reagent["vol"], capacity)
                    efficiency = tests / capacity
                    
                    if efficiency > best_efficiency:
                        best_efficiency = efficiency
                        best_loc = loc
            
            if best_loc is not None:
                best_locations.append(best_loc)
                available_locs.remove(best_loc)

        if len(best_locations) == num_reagents:
            self._place_reagent_set(exp, best_locations, config)
        else:
            raise ValueError(f"Could not find suitable locations for experiment {exp}")

    def _optimize_additional_sets(self, experiments, config):
        while config["available_locations"]:
            # Find experiment with lowest tests considering daily usage
            min_days_exp = min(
                experiments,
                key=lambda x: config["results"][x]["total_tests"] / config["daily_counts"][x] 
                if x in config["results"] else float('inf')
            )
            
            # Check if additional set would improve total tests
            exp_data = self.experiment_data[min_days_exp]
            num_reagents = len(exp_data["reagents"])
            
            if len(config["available_locations"]) >= num_reagents:
                # Calculate potential improvement
                available = sorted(config["available_locations"])
                potential_tests = float('inf')
                
                for reagent in exp_data["reagents"]:
                    loc = available[0]
                    capacity = self.get_location_capacity(loc)
                    tests = self.calculate_tests(reagent["vol"], capacity)
                    potential_tests = min(potential_tests, tests)
                
                current_tests = config["results"][min_days_exp]["total_tests"]
                daily_usage = config["daily_counts"][min_days_exp]
                current_days = current_tests / daily_usage
                potential_days = potential_tests / daily_usage
                
                # Only place additional set if it improves days of operation significantly
                if potential_days > current_days * 0.5:
                    locations = sorted(list(config["available_locations"]))[:num_reagents]
                    self._place_reagent_set(min_days_exp, locations, config)
                else:
                    break
            else:
                break

    def _place_reagent_set(self, exp_num, locations, config):
        exp = self.experiment_data[exp_num]
        sorted_reagents = sorted(exp["reagents"], key=lambda r: r["vol"], reverse=True)
        placements = []

        for i, reagent in enumerate(sorted_reagents):
            loc = locations[i]
            capacity = self.get_location_capacity(loc)
            tests = self.calculate_tests(reagent["vol"], capacity)
            
            placement = {
                "reagent_code": reagent["code"],
                "location": loc,
                "tests": tests,
                "volume": reagent["vol"]
            }
            placements.append(placement)
            
            config["tray_locations"][loc] = {
                "reagent_code": reagent["code"],
                "experiment": exp_num,
                "tests_possible": tests,
                "volume_per_test": reagent["vol"],
                "capacity": capacity
            }
            config["available_locations"].remove(loc)

        set_tests = min(p["tests"] for p in placements)
        
        if exp_num not in config["results"]:
            config["results"][exp_num] = {
                "name": exp["name"],
                "sets": [],
                "total_tests": 0
            }
        
        config["results"][exp_num]["sets"].append({
            "placements": placements,
            "tests_per_set": set_tests
        })
        config["results"][exp_num]["total_tests"] += set_tests

    def _calculate_days_of_operation(self, config):
        for exp_num, result in config["results"].items():
            daily_count = config["daily_counts"][exp_num]
            total_tests = result["total_tests"]
            days_of_operation = total_tests / daily_count
            result["daily_count"] = daily_count
            result["days_of_operation"] = round(days_of_operation, 1)

        # Calculate overall days of operation (minimum across all experiments)
        min_days = float('inf')
        for result in config["results"].values():
            days = result["days_of_operation"]
            if days < min_days:
                min_days = days
        
        config["overall_days_of_operation"] = round(min_days, 1)

    def get_available_experiments(self):
        return [{"id": id_, "name": exp["name"]} 
                for id_, exp in self.experiment_data.items()]

    def get_reagent_info(self, reagent_code):
        """
        Get information about a specific reagent code.
        """
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
        """
        Get capacity and other information about a specific location.
        """
        return {
            "location_number": location + 1,
            "capacity": self.get_location_capacity(location),
            "is_high_capacity": location < 4
        }
