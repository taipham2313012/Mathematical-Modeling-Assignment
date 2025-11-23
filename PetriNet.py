import numpy as np
import xml.etree.ElementTree as ET
from typing import List, Optional


class PetriNet:
    def __init__(
        self,
        place_ids: List[str],
        trans_ids: List[str],
        place_names: List[Optional[str]],
        trans_names: List[Optional[str]],
        I: np.ndarray,
        O: np.ndarray,
        M0: np.ndarray,
    ):
        self.place_ids = place_ids
        self.trans_ids = trans_ids
        self.place_names = place_names
        self.trans_names = trans_names
        self.I = I
        self.O = O
        self.M0 = M0

    @classmethod
    def from_pnml(cls, filename: str) -> "PetriNet":
        ## TODO read file PNML
        # Parse the XML file
        tree = ET.parse(filename)
        root = tree.getroot()

        # Define the namespace
        ns = {"pnml": "http://www.pnml.org/version-2009/grammar/pnml"}

        # Extract places
        place_ids = []
        place_names = []
        place_initial_markings = {}

        for place in root.findall(".//pnml:place", ns):
            place_id = place.get("id")
            place_ids.append(place_id)

            # Get place name
            name_elem = place.find(".//pnml:name/pnml:text", ns)
            place_name = name_elem.text if name_elem is not None else None
            place_names.append(place_name)

            # Get initial marking
            marking_elem = place.find(".//pnml:initialMarking/pnml:text", ns)
            marking = int(marking_elem.text) if marking_elem is not None else 0
            place_initial_markings[place_id] = marking

        # Extract transitions
        trans_ids = []
        trans_names = []

        for trans in root.findall(".//pnml:transition", ns):
            trans_id = trans.get("id")
            trans_ids.append(trans_id)

            # Get transition name
            name_elem = trans.find(".//pnml:name/pnml:text", ns)
            trans_name = name_elem.text if name_elem is not None else None
            trans_names.append(trans_name)

        # Create index mappings
        place_idx = {pid: i for i, pid in enumerate(place_ids)}
        trans_idx = {tid: i for i, tid in enumerate(trans_ids)}

        num_places = len(place_ids)
        num_trans = len(trans_ids)

        # Initialize I and O matrices with transposed dimensions
        # I and O should be (num_trans, num_places)
        I = np.zeros((num_trans, num_places), dtype=int)
        O = np.zeros((num_trans, num_places), dtype=int)

        # Extract arcs and build I and O matrices
        for arc in root.findall(".//pnml:arc", ns):
            source = arc.get("source")
            target = arc.get("target")

            # Check if arc is from place to transition (I matrix)
            if source in place_idx and target in trans_idx:
                p_idx = place_idx[source]
                t_idx = trans_idx[target]
                I[t_idx, p_idx] = 1

            # Check if arc is from transition to place (O matrix)
            elif source in trans_idx and target in place_idx:
                t_idx = trans_idx[source]
                p_idx = place_idx[target]
                O[t_idx, p_idx] = 1

        # Create initial marking vector M0
        M0 = np.array(
            [place_initial_markings.get(pid, 0) for pid in place_ids], dtype=int
        )

        return cls(place_ids, trans_ids, place_names, trans_names, I, O, M0)

    def __str__(self) -> str:
        s = []
        s.append("Places: " + str(self.place_ids))
        s.append("Place names: " + str(self.place_names))
        s.append("\nTransitions: " + str(self.trans_ids))
        s.append("Transition names: " + str(self.trans_names))
        s.append("\nI (input) matrix:")
        s.append(str(self.I))
        s.append("\nO (output) matrix:")
        s.append(str(self.O))
        s.append("\nInitial marking M0:")
        s.append(str(self.M0))
        return "\n".join(s)
