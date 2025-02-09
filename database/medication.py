from models.medication import Medication, MedicationTargetTime


def get_user_medication(user_id: str):
    medication = Medication()
    medicatinTimes = [MedicationTargetTime, MedicationTargetTime]

    return {"medication": medication, "medicationTime": medicatinTimes}