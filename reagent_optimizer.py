from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Union
from itertools import combinations
import json

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

    
    def _find_best_locations_for_experiment(self, exp_num, available_locations, daily_count):
        """Find optimal locations for an experiment considering high and low capacity combinations"""
        exp_data = self.experiment_data[exp_num]
        reagents = sorted(exp_data["reagents"], key=lambda r: r["vol"], reverse=True)
        num_reagents = len(reagents)
        
        best_locations = None
        best_tests = 0
    
        # Split available locations into high and low capacity
        high_cap_locs = [loc for loc in available_locations if loc < 4]
        low_cap_locs = [loc for loc in available_locations if loc >= 4]
        
        # For high-volume reagents, try using high-capacity locations first
        high_volume_reagents = [r for r in reagents if r["vol"] >= 1000]
        if high_volume_reagents and len(high_cap_locs) >= len(high_volume_reagents):
            remaining_reagents = [r for r in reagents if r["vol"] < 1000]
            high_locs = high_cap_locs[:len(high_volume_reagents)]
            
            # Try combinations of remaining locations for other reagents
            for low_locs in combinations(low_cap_locs, len(remaining_reagents)):
                test_locations = high_locs + list(low_locs)
                min_tests = float('inf')
                
                for reagent, loc in zip(reagents, test_locations):
                    capacity = self.get_location_capacity(loc)
                    tests = self.calculate_tests(reagent["vol"], capacity)
                    min_tests = min(min_tests, tests)
                
                if min_tests > best_tests:
                    best_tests = min_tests
                    best_locations = test_locations
        
        # Try all other possible combinations
        for high_count in range(min(len(high_cap_locs) + 1, num_reagents + 1)):
            low_count = num_reagents - high_count
            if low_count > len(low_cap_locs):
                continue
                
            for high_locs in combinations(high_cap_locs, high_count):
                for low_locs in combinations(low_cap_locs, low_count):
                    test_locations = list(high_locs) + list(low_locs)
                    min_tests = float('inf')
                    
                    for reagent, loc in zip(reagents, test_locations):
                        capacity = self.get_location_capacity(loc)
                        tests = self.calculate_tests(reagent["vol"], capacity)
                        min_tests = min(min_tests, tests)
                    
                    if min_tests > best_tests:
                        best_tests = min_tests
                        best_locations = test_locations
    
        return best_locations, best_tests

    def _calculate_experiment_tests(self, tray_locations, exp_num):
        """Calculate total tests possible for an experiment"""
        reagent_tests = defaultdict(int)
        exp_data = self.experiment_data[exp_num]
        
        # Sum up tests possible for each reagent
        for loc in tray_locations:
            if loc and loc["experiment"] == exp_num:
                reagent_tests[loc["reagent_code"]] += loc["tests_possible"]
        
        # Ensure we have all required reagents
        required_reagents = {r["code"] for r in exp_data["reagents"]}
        if not all(code in reagent_tests for code in required_reagents):
            return 0
            
        return (reagent_tests.values())

    def optimize_tray_configuration(self, selected_experiments, daily_counts):
        """Optimize tray configuration with enhanced two-phase approach"""
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
            "available_locations": list(range(self.MAX_LOCATIONS))
        }

        # Sort experiments by priority (daily count and volume)
        sorted_experiments = sorted(
            selected_experiments,
            key=lambda x: (
                daily_counts[x] * max(r["vol"] for r in self.experiment_data[x]["reagents"]),  # Combined priority
                len(self.experiment_data[x]["reagents"])  # More reagents last
            ),
            reverse=True
        )

        # Phase 1: Initial placement ensuring each experiment gets optimal locations
        for exp in sorted_experiments:
            num_reagents = len(self.experiment_data[exp]["reagents"])
            if num_reagents > len(config["available_locations"]):
                raise ValueError(f"Not enough locations available for experiment {exp}")

            best_locations, _ = self._find_best_locations_for_experiment(
                exp, config["available_locations"], daily_counts[exp]
            )

            if best_locations:
                self._place_reagent_set(config, exp, best_locations)
                config["available_locations"] = [
                    loc for loc in config["available_locations"] 
                    if loc not in best_locations
                ]

        # Phase 2: Fill remaining locations to maximize days of operation
        while config["available_locations"]:
            best_addition = None
            best_improvement = 0
            current_min_days = float('inf')

            # Find current minimum days
            for exp in selected_experiments:
                if exp in config["results"]:
                    tests = self._calculate_experiment_tests(config["tray_locations"], exp)
                    days = tests / daily_counts[exp]
                    current_min_days = min(current_min_days, days)

            # Try improving the limiting experiments first
            for exp in sorted_experiments:
                if exp not in config["results"]:
                    continue

                num_reagents = len(self.experiment_data[exp]["reagents"])
                if num_reagents > len(config["available_locations"]):
                    continue

                current_tests = self._calculate_experiment_tests(config["tray_locations"], exp)
                current_days = current_tests / daily_counts[exp]

                if current_days > current_min_days * 1.1:  # Skip if already 10% better than minimum
                    continue

                best_locations, additional_tests = self._find_best_locations_for_experiment(
                    exp, config["available_locations"], daily_counts[exp]
                )

                if best_locations:
                    new_days = (current_tests + additional_tests) / daily_counts[exp]
                    improvement = new_days - current_days

                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_addition = (exp, best_locations)

            if best_addition:
                exp, locations = best_addition
                self._place_reagent_set(config, exp, locations)
                config["available_locations"] = [
                    loc for loc in config["available_locations"] 
                    if loc not in locations
                ]
            else:
                break

        # Calculate final results
        self._calculate_final_results(config)
        return config


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

            if exp_num not in config["results"]:
                config["results"][exp_num] = {
                    "name": exp_data["name"],
                    "total_tests": 0,
                    "daily_count": config["daily_counts"][exp_num],
                    "days_of_operation": 0
                }

    def _calculate_final_results(self, config):
        """Calculate final results for all experiments"""
        for exp_num in config["results"].keys():
            total_tests = self._calculate_experiment_tests(config["tray_locations"], exp_num)
            days = total_tests / config["daily_counts"][exp_num]
            config["results"][exp_num].update({
                "total_tests": total_tests,
                "days_of_operation": days
            })

        config["overall_days_of_operation"] = min(
            result["days_of_operation"] 
            for result in config["results"].values()
        )

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
            return json.dumps(basic_info, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def __str__(self):
        """String representation of the optimizer"""
        return f"ReagentOptimizer(experiments={len(self.experiment_data)}, max_locations={self.MAX_LOCATIONS})"

    def __repr__(self):
        """Detailed string representation of the optimizer"""
        return f"ReagentOptimizer(experiments={len(self.experiment_data)}, max_locations={self.MAX_LOCATIONS})"
