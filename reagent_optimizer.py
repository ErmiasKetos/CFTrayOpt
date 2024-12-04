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
            11: {"name": "Total Alkalinity (LR)", "reagents": [{"code": "KR11E", "vol": 1000}]},
            12: {"name": "Orthophosphates-P (LR)", "reagents": [{"code": "KR12E1", "vol": 500}, {"code": "KR12E2", "vol": 500}, {"code": "KR12E3", "vol": 200}]},
            13: {"name": "Mercury (II)", "reagents": [{"code": "KR13E1", "vol": 850}, {"code": "KR13S", "vol": 300}]},
            14: {"name": "Selenium (IV)", "reagents": [{"code": "KR14E", "vol": 500}, {"code": "KR14S", "vol": 300}]},
            15: {"name": "Zinc (II) (LR)", "reagents": [{"code": "KR15E", "vol": 850}, {"code": "KR15S", "vol": 400}]},
            16: {"name": "Iron (Dissolved)", "reagents": [{"code": "KR16E1", "vol": 1000}, {"code": "KR16E2", "vol": 1000}, {"code": "KR16E3", "vol": 1000}, {"code": "KR16E4", "vol": 1000}]},
            17: {"name": "Residual Chlorine", "reagents": [{"code": "KR17E1", "vol": 1000}, {"code": "KR17E2", "vol": 1000}]},
            18: {"name": "Zinc (HR)", "reagents": [{"code": "KR18E1", "vol": 1000}, {"code": "KR18E2", "vol": 1000}]},
            19: {"name": "Manganese  (HR)", "reagents": [{"code": "KR19E1", "vol": 1000}, {"code": "KR19E2", "vol": 1000}, {"code": "KR19E3", "vol": 1000}]},
            20: {"name": "Orthophosphates-P (HR) ", "reagents": [{"code": "KR20E", "vol": 1600}]},
            21: {"name": "Total Alkalinity (HR)", "reagents": [{"code": "KR21E1", "vol": 1000}]},
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

    def calculate_days_for_volume(self, volume_ul, capacity_ml, daily_count):
        """Calculate days of operation for a given volume and daily usage"""
        tests = self.calculate_tests(volume_ul, capacity_ml)
        return tests / daily_count if daily_count > 0 else float('inf')

    def optimize_tray_configuration(self, selected_experiments, daily_counts):
        # Validate basic inputs
        for exp in selected_experiments:
            if exp not in self.experiment_data:
                raise ValueError(f"Invalid experiment number: {exp}")
            if exp not in daily_counts or daily_counts[exp] <= 0:
                raise ValueError(f"Invalid daily count for experiment {exp}")
    
        # Calculate initial reagents needed
        initial_reagents = sum(len(self.experiment_data[exp]["reagents"]) for exp in selected_experiments)
        
        # Initialize configuration
        config = {
            "tray_locations": [None] * self.MAX_LOCATIONS,
            "results": {},
            "available_locations": set(range(self.MAX_LOCATIONS)),
            "daily_counts": daily_counts
        }
    
        # Sort experiments by priority for initial placement
        sorted_experiments = self._sort_experiments_by_priority(selected_experiments, daily_counts)
    
        # Phase 1: Place primary sets for all selected experiments
        for exp in sorted_experiments:
            self._place_primary_set_days_optimized(exp, config)
    
        # Phase 2: Fill remaining locations optimizing for days of operation
        while config["available_locations"]:
            # Find experiment that would benefit most from additional sets
            best_exp = None
            best_improvement = 0
            
            for exp in selected_experiments:
                if len(self.experiment_data[exp]["reagents"]) <= len(config["available_locations"]):
                    current_days = (config["results"][exp]["total_tests"] / 
                                  config["daily_counts"][exp])
                    
                    # Calculate potential improvement
                    available_locs = sorted(config["available_locations"])
                    potential_days = self._calculate_potential_days(
                        exp,
                        available_locs[:len(self.experiment_data[exp]["reagents"])],
                        config["daily_counts"][exp]
                    )
                    
                    improvement = potential_days - current_days
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_exp = exp
    
            if best_exp and best_improvement > 0:
                self._place_primary_set_days_optimized(best_exp, config)
            else:
                # If no significant improvement possible, try to fill remaining slots
                # with the experiment that has the highest daily usage
                exp_with_highest_usage = max(
                    selected_experiments,
                    key=lambda x: config["daily_counts"][x]
                )
                if len(self.experiment_data[exp_with_highest_usage]["reagents"]) <= len(config["available_locations"]):
                    self._place_primary_set_days_optimized(exp_with_highest_usage, config)
                else:
                    break
    
        # Calculate final days of operation
        self._calculate_days_of_operation(config)
    
        return config

    def _sort_experiments_by_priority(self, experiments, daily_counts):
        """Sort experiments by priority considering days of operation potential"""
        experiment_metrics = []
        for exp in experiments:
            exp_data = self.experiment_data[exp]
            min_days = float('inf')
            for reagent in exp_data["reagents"]:
                days = self.calculate_days_for_volume(
                    reagent["vol"],
                    270,  # Use high-capacity location for comparison
                    daily_counts[exp]
                )
                min_days = min(min_days, days)
            
            experiment_metrics.append({
                'exp_id': exp,
                'reagent_count': len(exp_data["reagents"]),
                'daily_usage': daily_counts[exp],
                'potential_days': min_days,
                'max_volume': max(r["vol"] for r in exp_data["reagents"])
            })

        return [
            m['exp_id'] for m in sorted(
                experiment_metrics,
                key=lambda x: (
                    x['reagent_count'],
                    -x['daily_usage'],
                    -x['potential_days'],
                    x['max_volume']
                ),
                reverse=True
            )
        ]

    def _place_primary_set_days_optimized(self, exp, config):
        exp_data = self.experiment_data[exp]
        num_reagents = len(exp_data["reagents"])
        daily_count = config["daily_counts"][exp]

        available_locs = sorted(config["available_locations"])
        if len(available_locs) < num_reagents:
            raise ValueError(f"Not enough locations for experiment {exp}")

        best_locations = None
        best_days = 0
        
        sorted_reagents = sorted(exp_data["reagents"], key=lambda r: r["vol"], reverse=True)

        # Try high-capacity locations first for high-volume reagents
        high_volume_reagents = [r for r in sorted_reagents if r["vol"] > 800]
        if high_volume_reagents:
            available_270 = [loc for loc in range(4) if loc in config["available_locations"]]
            if len(available_270) >= len(high_volume_reagents):
                remaining_reagents = [r for r in sorted_reagents if r["vol"] <= 800]
                remaining_locs = [loc for loc in available_locs if loc not in available_270[:len(high_volume_reagents)]]
                
                if len(remaining_locs) >= len(remaining_reagents):
                    best_locations = (
                        available_270[:len(high_volume_reagents)] +
                        remaining_locs[:len(remaining_reagents)]
                    )

        # If no best locations found yet, try all available combinations
        if not best_locations:
            for i in range(len(available_locs) - num_reagents + 1):
                locations = available_locs[i:i + num_reagents]
                min_days = float('inf')
                
                for reagent, loc in zip(sorted_reagents, locations):
                    capacity = self.get_location_capacity(loc)
                    days = self.calculate_days_for_volume(reagent["vol"], capacity, daily_count)
                    min_days = min(min_days, days)
                
                if min_days > best_days:
                    best_days = min_days
                    best_locations = locations

        if best_locations:
            self._place_reagent_set(exp, best_locations, config)
        else:
            raise ValueError(f"Could not find suitable locations for experiment {exp}")

    def _optimize_additional_sets_days(self, experiments, config):
        while config["available_locations"]:
            min_days_exp = min(
                experiments,
                key=lambda x: config["results"][x]["total_tests"] / config["daily_counts"][x] 
                if x in config["results"] else float('inf')
            )
            
            exp_data = self.experiment_data[min_days_exp]
            num_reagents = len(exp_data["reagents"])
            
            if len(config["available_locations"]) >= num_reagents:
                current_days = (config["results"][min_days_exp]["total_tests"] / 
                              config["daily_counts"][min_days_exp])
                
                available_locs = sorted(config["available_locations"])
                potential_days = self._calculate_potential_days(
                    min_days_exp,
                    available_locs[:num_reagents],
                    config["daily_counts"][min_days_exp]
                )
                
                if potential_days > current_days * 0.25:
                    self._place_primary_set_days_optimized(min_days_exp, config)
                else:
                    break
            else:
                break

    def _calculate_potential_days(self, exp_num, locations, daily_count):
        """Calculate potential days of operation for a set of locations"""
        exp_data = self.experiment_data[exp_num]
        min_days = float('inf')
        
        for reagent, loc in zip(
            sorted(exp_data["reagents"], key=lambda r: r["vol"], reverse=True),
            locations
        ):
            capacity = self.get_location_capacity(loc)
            days = self.calculate_days_for_volume(reagent["vol"], capacity, daily_count)
            min_days = min(min_days, days)
            
        return min_days

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
        """Calculate days of operation for each experiment and overall"""
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

        # Adjust total tests possible based on overall days of operation
        for exp_num, result in config["results"].items():
            max_possible_tests = int(config["overall_days_of_operation"] * result["daily_count"])
            result["actual_total_tests"] = min(result["total_tests"], max_possible_tests)

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
