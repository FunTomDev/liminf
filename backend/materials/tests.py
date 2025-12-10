from django.test import TestCase
from .models import Material
from curriculum.models import Subject, Topic, Semester
import random

# Create your tests here.
def generator():
    """
    Generator function to yield a random number of materials.
    """
    # 1. Define sample data
    material_types = ['official', 'student_notes', 'mathpro']
    subject_names = ['TEST Matma', 'TEST Infa', 'TEST Fizyka']
    topic_names = ['TEST Teoria', 'TEST Zadania', 'TEST Laboratoria']

    # 2. Create test subjects and topics
    subjects = []
    topics = []

    for subject_name in subject_names:
        subject, _ = Subject.objects.get_or_create(name=subject_name, semester=Semester.objects.get_or_create(degree_type="I", number=random.randint(1,7))[0])
        subjects.append(subject)
        for topic_name in topic_names:
            print(f"Creating topic: {topic_name} for subject: {subject_name}")
            topic, _ = Topic.objects.get_or_create(name=topic_name, subject=subject)
            topics.append(topic)

    # 3. Create fake materials
    for i in range(int(input("How many materials do you want to generate?: "))):  # Adjust quantity as needed
        topic = random.choice(topics)
        mat_type = random.choice(material_types)
        title = f"TEST Material {i}"

        Material.objects.create(
            topic=topic,
            title=title,
            type=mat_type,
            description="To jest przykładowy opis testowego materiału.",
            content="Testowa zawartość materiału.",
        )

    print("✅ Test materials, topics and subjects created.")

def delete_generated_values():
    # Delete test materials
    mat_count, _ = Material.objects.filter(title__startswith="TEST ").delete()

    # Delete test topics and subjects
    topic_count, _ = Topic.objects.filter(name__startswith="TEST ").delete()
    subj_count, _ = Subject.objects.filter(name__startswith="TEST ").delete()

    print(f"🧼 Deleted {mat_count} materials, {topic_count} topics, and {subj_count} subjects.")

ans = input("Do you want to generate test materials? (y/n): ").strip().lower()
if ans == 'y':
    generator()
elif ans == 'n':
    delete_generated_values()
else:
    print("Invalid input. Please enter 'y' or 'n'.")
