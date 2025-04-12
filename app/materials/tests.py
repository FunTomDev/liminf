from django.test import TestCase
from .models import Subject, Topic, Material
import random

# Create your tests here.
def generator():
    """
    Generator function to yield a random number of materials.
    """
    # 1. Define sample data
    material_types = ['official', 'student_notes']
    subject_names = ['TEST_Matma', 'TEST_Infa', 'TEST_Fizyka']
    topic_names = ['TEST_Teoria', 'TEST_Zadania', 'TEST_Laboratoria']

    # 2. Create test subjects and topics
    subjects = []
    topics = []

    for subject_name in subject_names:
        subject, _ = Subject.objects.get_or_create(name=subject_name)
        subjects.append(subject)
        for topic_name in topic_names:
            full_topic_name = f"{topic_name}_{subject.slug}"
            topic, _ = Topic.objects.get_or_create(name=full_topic_name, subject=subject)
            topics.append(topic)

    # 3. Create fake materials
    for i in range(int(input("How many materials do you want to generate?: "))):  # Adjust quantity as needed
        topic = random.choice(topics)
        mat_type = random.choice(material_types)
        title = f"TEST_Material_{i}_{topic.slug}"

        Material.objects.create(
            topic=topic,
            title=title,
            type=mat_type,
            short_description="To jest przykładowy opis testowego materiału.",
            content="Testowa zawartość materiału.",
            file=None  # Optional: can point to dummy file if needed
        )

    print("✅ Test materials, topics and subjects created.")

def delete_generated_values():
    # Delete test materials
    mat_count, _ = Material.objects.filter(title__startswith="TEST_").delete()

    # Delete test topics and subjects
    topic_count, _ = Topic.objects.filter(name__startswith="TEST_").delete()
    subj_count, _ = Subject.objects.filter(name__startswith="TEST_").delete()

    print(f"🧼 Deleted {mat_count} materials, {topic_count} topics, and {subj_count} subjects.")

ans = input("Do you want to generate test materials? (y/n): ").strip().lower()
if ans == 'y':
    generator()
elif ans == 'n':
    delete_generated_values()
else:
    print("Invalid input. Please enter 'y' or 'n'.")
