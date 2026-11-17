"""Configuration StrictDoc du projet PersoCAO.

Lue automatiquement par `strictdoc export .` et `strictdoc server .`
lancés à la racine du dépôt.
"""

from strictdoc.core.project_config import ProjectConfig


def create_config() -> ProjectConfig:
    return ProjectConfig(
        project_title="PersoCAO – Exigences",
        # Les exigences font foi dans reqs/ (une source .sdoc par niveau du V).
        include_doc_paths=["reqs/**"],
        dir_for_sdoc_cache="build/_cache",
        project_features=[
            # Écrans standard.
            "TABLE_SCREEN",
            "TRACEABILITY_SCREEN",
            "DEEP_TRACEABILITY_SCREEN",
            "SEARCH",
            # Matrice de traçabilité et statistiques (fonctions expérimentales).
            "TRACEABILITY_MATRIX_SCREEN",
            "PROJECT_STATISTICS_SCREEN",
            # Traçabilité exigences -> code et tests, prête pour le V montant :
            # un commentaire `@relation(BES-F-01, scope=function)` dans un
            # fichier source ou de test le relie à l'exigence.
            "REQUIREMENT_TO_SOURCE_TRACEABILITY",
        ],
        # Code et tests analysés pour la traçabilité (dossiers créés à
        # l'implémentation, après la fin du V descendant).
        source_root_path=".",
        include_source_paths=["src/**", "modules/**", "tests/**"],
        exclude_source_paths=["build/**"],
    )
