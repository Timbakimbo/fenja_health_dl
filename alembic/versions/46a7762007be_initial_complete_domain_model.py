"""initial_complete_domain_model

Revision ID: 46a7762007be
Revises: 
Create Date: 2026-03-04 17:26:29.348046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46a7762007be'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Keine FK-Abhängigkeiten ──────────────────────────────────────────────
    op.create_table(
        "health_markers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("ctli", sa.Float(), nullable=True, comment="Canine TLI in µg/L; EPI threshold < 2.5"),
        sa.Column("lipase", sa.Float(), nullable=True, comment="Lipase in U/L"),
        sa.Column("amylase", sa.Float(), nullable=True, comment="Amylase in U/L"),
        sa.Column("cobalamin_b12", sa.Float(), nullable=True, comment="Cobalamin B12 in pg/mL"),
        sa.Column("folate", sa.Float(), nullable=True, comment="Folate in µg/L"),
        sa.Column("glucose", sa.Float(), nullable=True, comment="Glucose in mg/dL"),
        sa.Column("vitamin_e", sa.Float(), nullable=True, comment="Vitamin E in mg/L"),
        sa.Column("vitamin_k", sa.Float(), nullable=True, comment="Vitamin K in µg/L"),
    )

    op.create_table(
        "vital_readings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("marker_type", sa.Text(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("unit", sa.Text(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    op.create_table(
        "vet_visits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("vet_name", sa.Text(), nullable=True),
        sa.Column("clinic", sa.Text(), nullable=True),
        sa.Column("diagnosis", sa.Text(), nullable=True),
        sa.Column("findings", sa.Text(), nullable=True),
        sa.Column("next_appointment", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    op.create_table(
        "daily_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("date", sa.Date(), nullable=False, unique=True),
        # Ernährung
        sa.Column("food_offered_g", sa.Float(), nullable=True),
        sa.Column("food_eaten_g", sa.Float(), nullable=True),
        sa.Column("water_intake", sa.String(20), nullable=True, comment="normal | erhöht | reduziert"),
        # Verdauung (EPI-spezifisch)
        sa.Column("stool_consistency", sa.Integer(), nullable=True),
        sa.Column("stool_color", sa.String(20), nullable=True, comment="normal | blass | fettig | dunkel"),
        sa.Column("flatulence", sa.Boolean(), nullable=True),
        sa.Column("vomiting", sa.Boolean(), nullable=True),
        sa.Column("vomiting_count", sa.Integer(), nullable=True),
        # Energie & Verhalten (1-5)
        sa.Column("energy_level", sa.Integer(), nullable=True),
        sa.Column("willingness_to_walk", sa.Integer(), nullable=True),
        sa.Column("play_interest", sa.Integer(), nullable=True),
        # Äußeres Erscheinungsbild (1-5)
        sa.Column("coat_condition", sa.Integer(), nullable=True),
        sa.Column("muscle_wasting", sa.Integer(), nullable=True),
        # Orthopädie
        sa.Column("lameness_score", sa.Integer(), nullable=True, comment="0=keine Lahmheit, 4=keine Belastung"),
        sa.Column("affected_limb", sa.String(10), nullable=True, comment="VL | VR | HL | HR"),
        sa.Column("stiffness_after_rest", sa.Boolean(), nullable=True),
        # Schmerz (Glasgow CMPS-SF: 0-24)
        sa.Column("pain_score", sa.Integer(), nullable=True, comment="Glasgow CMPS-SF: 0-24, Intervention ab 6"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        # Check constraints
        sa.CheckConstraint("stool_consistency BETWEEN 1 AND 5", name="ck_stool_1_5"),
        sa.CheckConstraint("energy_level BETWEEN 1 AND 5", name="ck_energy_1_5"),
        sa.CheckConstraint("willingness_to_walk BETWEEN 1 AND 5", name="ck_walk_1_5"),
        sa.CheckConstraint("play_interest BETWEEN 1 AND 5", name="ck_play_1_5"),
        sa.CheckConstraint("coat_condition BETWEEN 1 AND 5", name="ck_coat_1_5"),
        sa.CheckConstraint("muscle_wasting BETWEEN 1 AND 5", name="ck_muscle_1_5"),
        sa.CheckConstraint("lameness_score BETWEEN 0 AND 4", name="ck_lameness_0_4"),
        sa.CheckConstraint("pain_score BETWEEN 0 AND 24", name="ck_pain_0_24"),
        sa.CheckConstraint("vomiting_count >= 0", name="ck_vomiting_count_pos"),
    )

    op.create_table(
        "treatment_templates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False, unique=True),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("default_schedule", sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # ── FK-Abhängigkeiten ───────────────────────────────────────────────────
    op.create_table(
        "symptom_observations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("daily_log_id", sa.Integer(), sa.ForeignKey("daily_logs.id"), nullable=False),
        sa.Column("symptom_type", sa.String(100), nullable=False, comment="z.B. hautausschlag, niesen, zittern"),
        sa.Column("value_numeric", sa.Float(), nullable=True),
        sa.Column("value_text", sa.String(200), nullable=True),
        sa.Column("value_bool", sa.Boolean(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "treatment_protocols",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("template_id", sa.Integer(), sa.ForeignKey("treatment_templates.id"), nullable=True),
        sa.Column("vet_visit_id", sa.Integer(), sa.ForeignKey("vet_visits.id"), nullable=True),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("schedule", sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("prescribed_by", sa.String(200), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "treatment_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("protocol_id", sa.Integer(), sa.ForeignKey("treatment_protocols.id"), nullable=False),
        sa.Column("scheduled_date", sa.Date(), nullable=False),
        sa.Column("administered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("dose", sa.Float(), nullable=True),
        sa.Column("unit", sa.String(50), nullable=True),
        sa.Column("administered_by", sa.String(100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    # In umgekehrter FK-Reihenfolge droppen
    op.drop_table("treatment_entries")
    op.drop_table("treatment_protocols")
    op.drop_table("symptom_observations")
    op.drop_table("treatment_templates")
    op.drop_table("daily_logs")
    op.drop_table("vet_visits")
    op.drop_table("vital_readings")
    op.drop_table("health_markers")
