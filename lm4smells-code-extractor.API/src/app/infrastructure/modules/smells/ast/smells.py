from infrastructure.service.metric_codes.ast_analyzer import ASTAnalyzer
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from domain.entities.smell_occurrence import SmellOccurrence
from uuid import uuid4
from domain.value_objects.smell_type import SmellType
from domain.value_objects.location import Location
from domain.value_objects.metrics import Metrics
from domain.value_objects.author import Author
import ast


class Smells:
    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()

    def long_parameter_list(self, task_id: str, file_contents: List[str], file_names: List[str], max_parameters: int = 4):
    
        smells: List[SmellOccurrence] = []
        files_data = self.ast_analyzer.count_parameters_from_sources(file_contents, file_names)

        for file_name, methods in files_data.items():
            for method in methods:
                total = method["parameters"]["total"]
                
                if total > max_parameters:
                    smell_type = SmellType.LONG_PARAMETER_LIST.value
                    description = f"Method '{method['name']}' has {total} parameters."
                else:
                    smell_type = SmellType.NO_LONG_PARAMETER_LIST.value
                    description = f"Method '{method['name']}' has {total} parameters."

                smells.append(
                    SmellOccurrence(
                        id=task_id,
                        definition_author="Scylla",
                        smell_type=smell_type,
                        description=description,
                        location=Location(
                            file_name=file_name,
                            start_line=method["line"],
                            end_line=method["line"],
                        ),
                        metrics=Metrics(PAR=total),
                    )
                )

        return smells
    
    def long_method(self, task_id: str, file_contents: List[str], file_names: List[str], max_lines: int = 67):
        smells: List[SmellOccurrence] = []
        
        for file_name, content in zip(file_names, file_contents):
            lines = content.splitlines()
            parameters_data = self.ast_analyzer.count_parameters_from_sources([content], [file_name])
            parameters_data = parameters_data.get(file_name, [])

            current_function = None

            for i, line in enumerate(lines):
                stripped_line = line.strip()

                if stripped_line.startswith("def "):
                    
                    if current_function:
                        start_line = current_function["start"]
                        end_line = i - 1
                        loc, total_lines = self.ast_analyzer.calculate_loc_and_total(lines[start_line:end_line])

                        method_par = next(
                            (m["parameters"]["total"] for m in parameters_data if m["line"] == start_line + 1),
                            0
                        )

                        if total_lines > max_lines:
                            smell_type = SmellType.LONG_METHOD.value
                            description = f"Method '{current_function['name']}' too long: {total_lines} lines (max: {max_lines})."
                        else:
                            smell_type = SmellType.NO_LONG_METHOD.value
                            description = f"Method '{current_function['name']}' has {total_lines} lines."

                        smells.append(
                            SmellOccurrence(
                                id=task_id,
                                definition_author="Scylla",
                                smell_type=smell_type,
                                description=description,
                                location=Location(
                                    file_name=file_name,
                                    start_line=start_line + 1,
                                    end_line=end_line + 1,
                                ),
                                metrics=Metrics(MLOC=total_lines, PAR=method_par),
                            )
                        )

                    
                    method_name = stripped_line.split("def ")[1].split("(")[0].strip()
                    current_function = {"name": method_name, "start": i}

            
            if current_function:
                start_line = current_function["start"]
                end_line = len(lines) - 1
                loc, total_lines = self.ast_analyzer.calculate_loc_and_total(lines[start_line:end_line])

                method_par = next(
                    (m["parameters"]["total"] for m in parameters_data if m["line"] == start_line + 1),
                    0
                )

                if total_lines > max_lines:
                    smell_type = SmellType.LONG_METHOD.value
                    description = f"Method '{current_function['name']}' too long: {total_lines} lines (max: {max_lines})."
                else:
                    smell_type = SmellType.NO_LONG_METHOD.value
                    description = f"Method '{current_function['name']}' has {total_lines} lines."

                smells.append(
                    SmellOccurrence(
                        id=task_id,
                        definition_author="Scylla",
                        smell_type=smell_type,
                        description=description,
                        location=Location(
                            file_name=file_name,
                            start_line=start_line + 1,
                            end_line=end_line + 1,
                        ),
                        metrics=Metrics(MLOC=total_lines, PAR=method_par),
                    )
                )

        return smells
    
    def large_class(
        self,
        task_id: str,
        file_contents: List[str],
        file_names: List[str],
        max_lines: int = 200,
        max_attributes_methods: int = 40,
    ):
        smells: List[SmellOccurrence] = []

        

        for file_name, content in zip(file_names, file_contents):
            
            
            try:
                max_lines = int(max_lines)
                max_attrs = int(max_attributes_methods)
            except (TypeError, ValueError):
                max_lines, max_attrs = 200, 40

            
            noa_stats = self.ast_analyzer.count_attributes(content, file_name)
            nom_stats = self.ast_analyzer.count_methods(content, file_name)
            
            


            class_locs = {}
        
            for class_name, metrics_data in nom_stats.items():
                start_line = metrics_data.get("start_line", 1)
                loc = self.ast_analyzer.count_class_loc(content, file_name, start_line - 1)
                class_locs[class_name] = loc

            for class_name, metrics_data in nom_stats.items():
                total_attrs = noa_stats.get(class_name, {}).get("total_attributes", 0)
                total_methods = metrics_data.get("total_methods", 0)
                loc = class_locs.get(class_name, 0)

                if (total_attrs + total_methods) > max_attrs or loc > max_lines:
                    smell_type = SmellType.LARGE_CLASS.value
                    description = (
                        f"Class '{class_name}' is too large: "
                        f"Attributes={total_attrs}, Methods={total_methods}, LOC={loc}"
                    )
                else:
                    smell_type = SmellType.NO_LARGE_CLASS.value
                    description = (
                        f"Class '{class_name}' is within limits: "
                        f"Attributes={total_attrs}, Methods={total_methods}, LOC={loc}"
                    )


                smells.append(
                    SmellOccurrence(
                        id=task_id,
                        definition_author="Scylla",
                        smell_type=smell_type,
                        description=description,
                        location=Location(
                            file_name=file_name,
                            start_line=metrics_data.get("start_line", 1),
                            end_line=metrics_data.get("start_line", 1) + loc - 1 if loc > 0 else 1,
                        ),
                        metrics=Metrics(
                            MLOC=loc,
                            NOA=total_attrs,
                            NOM=total_methods,
                        ),
                    )
                )

        return smells

    def data_class(
        self,
        task_id: str,
        file_content: str,
        filename: str,
        lwmc_threshold: int = 50,
        lcom_threshold: float = 0.8
    ):
        noa_stats = self.ast_analyzer.count_attributes(file_content, filename)
        nom_stats = self.ast_analyzer.count_methods(file_content, filename)
        lwmc_stats = self.ast_analyzer.calculate_lwmc(file_content, filename)
        lcom_stats = self.ast_analyzer.calculate_lcom(file_content, filename)

        smells: List[SmellOccurrence] = []

        for class_name in nom_stats.keys():
            start_line = nom_stats[class_name]["start_line"]
            loc = self.ast_analyzer.count_class_loc(file_content, filename, start_line - 1)

            noa = noa_stats.get(class_name, {}).get("total_attributes", 0)
            nom = nom_stats[class_name]["total_methods"]
            lwmc = lwmc_stats.get(class_name, 0)
            lcom = lcom_stats.get(class_name, 0.0)

            if lwmc > lwmc_threshold or lcom > lcom_threshold:
                smell_type = SmellType.DATA_CLASS.value
                description = (
                    f"Class '{class_name}' with Data Class characteristics - "
                    f"LWMC={lwmc}, LCOM={lcom:.2f}, "
                    f"Attributes={noa}, Methods={nom}, Lines={loc}"
                )
            else:
                smell_type = SmellType.NO_DATA_CLASS.value
                description = (
                    f"Class '{class_name}' without Data Class characteristics - "
                    f"LWMC={lwmc}, LCOM={lcom:.2f}, "
                    f"Attributes={noa}, Methods={nom}, Lines={loc}"
                )

            smells.append(
                SmellOccurrence(
                    id=task_id,
                    smell_type=smell_type,
                    description=description,
                    location=Location(
                        file_name=filename.replace("\\", "/"),
                        start_line=start_line,
                        end_line=start_line + loc - 1
                    ),
                    metrics=Metrics(
                        MLOC=loc,
                        NOA=noa,
                        NOM=nom,
                        LWMC=lwmc,
                        LCOM=lcom
                    ),
                    definition_author="Scylla",
                    threshold_used=max(lwmc_threshold, lcom_threshold)
                )
            )

        return smells


    def lazy_class(self, task_id: str, file_contents: Union[str, List[str]], file_names: Union[str, List[str]]) -> List[SmellOccurrence]:
        
        if isinstance(file_contents, str):
            file_contents = [file_contents]
        if isinstance(file_names, str):
            file_names = [file_names]

        smells: List[SmellOccurrence] = []

        for file_content, file_name in zip(file_contents, file_names):
            noa_stats = self.ast_analyzer.count_attributes(file_content, file_name)
            nom_stats = self.ast_analyzer.count_methods(file_content, file_name)

            for class_name, metrics in nom_stats.items():
                nom = metrics["total_methods"]
                noa = noa_stats.get(class_name, {}).get("total_attributes", 0)
                dit = self.ast_analyzer.calculate_dit(file_content, file_name, class_name)

                loc = self.ast_analyzer.count_class_loc(file_content, file_name, metrics["start_line"] - 1)

                if (nom < 5 and noa < 5) or dit < 2:
                    smell_type = SmellType.LAZY_CLASS.value
                    description = f"Class '{class_name}' is lazy: NOM={nom}, NOA={noa}, DIT={dit}, LOC={loc}"
                else:
                    smell_type = SmellType.NO_LAZY_CLASS.value
                    description = f"Class '{class_name}' is not lazy: NOM={nom}, NOA={noa}, DIT={dit}, LOC={loc}"

                smells.append(
                    SmellOccurrence(
                        id=task_id,
                        definition_author="Scylla",
                        smell_type=smell_type,
                        description=description,
                        location=Location(
                            file_name=file_name,
                            start_line=metrics["start_line"],
                            end_line=metrics["start_line"] + loc - 1,
                        ),
                        metrics=Metrics(
                            NOM=nom,
                            NOA=noa,
                            DIT=dit,
                            MLOC=loc,
                        ),
                    )
                )

        return smells

    def magic_numbers(self, task_id: str, file_content: str, filename: str) -> List[SmellOccurrence]:
        MAGIC_NUMBER_EXCEPTIONS = {0.0, 1.0, -1.0}

        tree = self.ast_analyzer.parse_source(file_content, filename)
        smells: List[SmellOccurrence] = []
        for val, holder, parent in self.ast_analyzer.iter_numeric_literals(tree):
            if val in MAGIC_NUMBER_EXCEPTIONS:
                is_magic = False
            elif self.ast_analyzer.is_constant_assignment(parent) or self.ast_analyzer.is_parameter_default(parent):
                is_magic = False
            else:
                is_magic = True

            smell_type = SmellType.MAGIC_NUMBERS.value if is_magic else SmellType.NO_MAGIC_NUMBERS.value
            description = (
                f"Magic number found: {val}"
                if is_magic
                else f"Number '{val}' is not considered magic"
            )

            smells.append(
                SmellOccurrence(
                    id=task_id,
                    smell_type=smell_type,
                    description=description,
                    location=Location(
                        file_name=filename,
                        start_line=getattr(holder, "lineno", 0),
                        end_line=getattr(holder, "lineno", 0),
                    ),
                    metrics=Metrics(),
                    definition_author="Scylla",
                )
            )

        return smells


    def _is_valid_magic_number(self, parent_node):
        if parent_node is None:
            return True

        
        if isinstance(parent_node, ast.Assign):
            return not any(
                isinstance(target, ast.Name) and target.id.isupper()
                for target in parent_node.targets
            )

        
        return not isinstance(parent_node, ast.arg)

