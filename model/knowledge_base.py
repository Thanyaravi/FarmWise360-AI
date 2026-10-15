"""
FarmWise 360 AI - Agricultural Verified Knowledge Base (Edge-RAG Store)
Provides zero-hallucination, agronomist-verified treatment protocols,
active ingredients, organic alternatives, and prevention practices.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import re


@dataclass
class DiseaseAdvisory:
    crop: str
    condition: str
    severity: str
    symptoms: List[str]
    treatment_chemical: str
    treatment_organic: str
    prevention: str
    confidence_threshold: float = 0.60


class AgriculturalKnowledgeBase:
    """In-memory local verified agricultural advisory knowledge store."""

    def __init__(self):
        self._database: Dict[str, DiseaseAdvisory] = {}
        self._load_verified_knowledge()

    def _key(self, crop: str, condition: str) -> str:
        return f"{crop.strip().lower()}::{condition.strip().lower()}"

    def _load_verified_knowledge(self):
        records = [
            DiseaseAdvisory(
                crop="Tomato",
                condition="Early Blight",
                severity="Medium",
                symptoms=["brown circular spots", "target-like rings", "lower leaves yellowing", "stem lesions"],
                treatment_chemical="Spray Mancozeb 75% WP @ 2.5g/L or Chlorothalonil 75% WP @ 2g/L water at 10-day intervals.",
                treatment_organic="Apply Trichoderma viride @ 5g/L or spray 5% Neem seed kernel extract (NSKE).",
                prevention="Practice 3-year crop rotation with non-solanaceous crops; use drip irrigation to prevent splash dispersal.",
            ),
            DiseaseAdvisory(
                crop="Tomato",
                condition="Late Blight",
                severity="High",
                symptoms=["water-soaked dark spots", "white fungal growth under leaf", "rapid browning", "fruit rot"],
                treatment_chemical="Spray Metalaxyl 8% + Mancozeb 64% WP @ 2.5g/L or Cymoxanil + Mancozeb @ 2g/L immediately.",
                treatment_organic="Spray Copper hydroxide or Bordeaux mixture (1%) as prophylactic barrier.",
                prevention="Destroy infected haulms; avoid overhead irrigation; ensure wide field spacing for air circulation.",
            ),
            DiseaseAdvisory(
                crop="Tomato",
                condition="Healthy",
                severity="Low",
                symptoms=["vibrant green foliage", "vigorous growth", "no spotting or curling"],
                treatment_chemical="No chemical treatment required.",
                treatment_organic="Maintain balanced organic compost and seaweed extract foliar spray every 15 days.",
                prevention="Continue regular scouting and balanced N-P-K fertigation.",
            ),
            DiseaseAdvisory(
                crop="Wheat",
                condition="Leaf Rust",
                severity="High",
                symptoms=["orange-brown pustules", "powdery spots on leaf blade", "premature leaf drying"],
                treatment_chemical="Apply Propiconazole 25% EC @ 1ml/L or Tebuconazole 250 EC @ 1ml/L at first appearance.",
                treatment_organic="Apply cow urine spray (10%) fermented with neem leaf extract for mild prophylactic control.",
                prevention="Sow rust-resistant wheat varieties (e.g., HD-2967, DBW-187); avoid excessive nitrogenous fertilizers.",
            ),
            DiseaseAdvisory(
                crop="Wheat",
                condition="Powdery Mildew",
                severity="Medium",
                symptoms=["white powdery patches on leaves", "stems coated with gray-white mold", "stunted spike growth"],
                treatment_chemical="Spray Wettable Sulphur 80% WP @ 3g/L or Hexaconazole 5% EC @ 1ml/L water.",
                treatment_organic="Foliar spray of diluted milk whey (1:9 ratio with water) or potassium bicarbonate solution.",
                prevention="Avoid dense sowing; ensure optimal sunlight penetration through row spacing.",
            ),
            DiseaseAdvisory(
                crop="Wheat",
                condition="Healthy",
                severity="Low",
                symptoms=["uniform green canopy", "erect tillers", "clean leaf sheaths"],
                treatment_chemical="No chemical treatment required.",
                treatment_organic="Apply balanced micronutrient spray (Zinc + Iron) during tillering stage.",
                prevention="Maintain recommended irrigation schedule at critical growth stages (CRI, flowering).",
            ),
            DiseaseAdvisory(
                crop="Rice",
                condition="Bacterial Leaf Blight",
                severity="High",
                symptoms=["yellow wavy margins on leaf tips", "milky bacterial ooze early morning", "straw-colored wilting"],
                treatment_chemical="Spray Streptocycline @ 0.1g/L combined with Copper Oxychloride 50% WP @ 2.5g/L.",
                treatment_organic="Spray fresh cow dung slurry supernatant (20%) or Pseudomonas fluorescens @ 10g/L.",
                prevention="Drain stagnant water; apply potassium fertilizer to strengthen cell walls; avoid top-dressing excess nitrogen.",
            ),
            DiseaseAdvisory(
                crop="Rice",
                condition="Blast",
                severity="High",
                symptoms=["spindle-shaped lesions with gray centers", "neck rot turning black", "panicle shattering"],
                treatment_chemical="Spray Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5ml/L at early tillering.",
                treatment_organic="Treat seeds with Pseudomonas fluorescens @ 10g/kg; spray seaweed extract.",
                prevention="Avoid nursery moisture stress; maintain thin water layer in field; use blast-tolerant seed lots.",
            ),
            DiseaseAdvisory(
                crop="Rice",
                condition="Healthy",
                severity="Low",
                symptoms=["deep green leaves", "strong active tillers", "clean panicles"],
                treatment_chemical="No chemical treatment required.",
                treatment_organic="Maintain azolla biofertilizer in standing water.",
                prevention="Standard alternate wetting and drying (AWD) water management.",
            ),
            DiseaseAdvisory(
                crop="Potato",
                condition="Late Blight",
                severity="Critical",
                symptoms=["water-soaked brown-black spots", "white mildew on undersides", "foul-smelling decaying tubers"],
                treatment_chemical="Prophylactic spray of Mancozeb 75% WP @ 2.5g/L; curative spray of Dimethomorph 50% WP @ 1g/L.",
                treatment_organic="Spray Bordeaux mixture 1% before rainy spells; apply bio-fungicide Trichoderma harzianum.",
                prevention="Use certified disease-free seed tubers; earth up soil well to protect tubers from surface spores.",
            ),
            DiseaseAdvisory(
                crop="Potato",
                condition="Healthy",
                severity="Low",
                symptoms=["healthy green bush canopy", "stout stems", "clean foliage"],
                treatment_chemical="No chemical treatment required.",
                treatment_organic="Apply compost tea and vermicompost top dressing.",
                prevention="Proper earthing up and regulated furrow irrigation.",
            ),
            DiseaseAdvisory(
                crop="Cotton",
                condition="Bacterial Blight",
                severity="High",
                symptoms=["angular water-soaked leaf spots", "black vein blight", "boll lesions"],
                treatment_chemical="Spray Copper Oxychloride 50% WP @ 2.5g/L mixed with Streptocycline @ 100ppm (1g/10L).",
                treatment_organic="Foliar spray with Pseudomonas fluorescens @ 5g/L or Neem oil 1500ppm @ 3ml/L.",
                prevention="Delint seed with concentrated sulfuric acid before sowing; destroy crop residue after harvest.",
            ),
            DiseaseAdvisory(
                crop="Cotton",
                condition="Healthy",
                severity="Low",
                symptoms=["robust vegetative frame", "clean squares and bolls", "healthy foliage"],
                treatment_chemical="No chemical treatment required.",
                treatment_organic="Pheromone traps for pest surveillance and neem spray.",
                prevention="Integrated Pest Management (IPM) monitoring.",
            ),
        ]

        for advisory in records:
            key = self._key(advisory.crop, advisory.condition)
            self._database[key] = advisory

    def get_advisory(self, crop: str, condition: str) -> Optional[DiseaseAdvisory]:
        """Fetch exact verified advisory by crop and diagnosed condition."""
        return self._database.get(self._key(crop, condition))

    def search_by_symptoms(self, query_text: str) -> List[DiseaseAdvisory]:
        """Keyword-grounded semantic search across verified symptom profiles."""
        tokens = set(re.findall(r"\w+", query_text.lower()))
        scores = []

        for advisory in self._database.values():
            symptom_text = " ".join(advisory.symptoms).lower()
            match_count = sum(1 for token in tokens if token in symptom_text)
            if match_count > 0:
                scores.append((match_count, advisory))

        scores.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scores[:3]]

    def list_supported_crops(self) -> List[str]:
        return sorted(list({adv.crop for adv in self._database.values()}))

    def list_supported_conditions(self, crop: Optional[str] = None) -> List[str]:
        if crop:
            return sorted(
                list({adv.condition for adv in self._database.values() if adv.crop.lower() == crop.lower()})
            )
        return sorted(list({adv.condition for adv in self._database.values()}))
