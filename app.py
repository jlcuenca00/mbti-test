from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secretkey123'

questions = [
    {"q": "At a party, you’re more likely to:", "dimension": "EI", "a": ("E", "Mingle with everyone"), "b": ("I", "Stick to a few close friends")},
    {"q": "When tackling a new project, you prefer to:", "dimension": "SN", "a": ("S", "Use tried-and-true methods"), "b": ("N", "Experiment with new ideas")},
    {"q": "You’re more influenced by:", "dimension": "TF", "a": ("T", "Logical reasoning"), "b": ("F", "Personal values and emotions")},
    {"q": "When making plans, you tend to:", "dimension": "JP", "a": ("J", "Schedule everything in advance"), "b": ("P", "Keep it flexible and spontaneous")},
    {"q": "In group discussions, you usually:", "dimension": "EI", "a": ("E", "Talk and lead"), "b": ("I", "Listen more than talk")},
    {"q": "You’re more drawn to:", "dimension": "SN", "a": ("S", "Concrete facts"), "b": ("N", "Abstract theories")},
    {"q": "In conflict situations, you rely on:", "dimension": "TF", "a": ("T", "Objective analysis"), "b": ("F", "Empathy and harmony")},
    {"q": "When approaching tasks, you:", "dimension": "JP", "a": ("J", "Like clear deadlines"), "b": ("P", "Prefer to go with the flow")},
    {"q": "When meeting new people, you:", "dimension": "EI", "a": ("E", "Start conversations easily"), "b": ("I", "Wait for others to approach")},
    {"q": "You process information through:", "dimension": "SN", "a": ("S", "Step-by-step details"), "b": ("N", "Big-picture patterns")},
    {"q": "In decisions, you value:", "dimension": "TF", "a": ("T", "Fairness and consistency"), "b": ("F", "Compassion and kindness")},
    {"q": "Your desk is usually:", "dimension": "JP", "a": ("J", "Neat and organized"), "b": ("P", "Creative chaos")},
    {"q": "You recharge by:", "dimension": "EI", "a": ("E", "Being with others"), "b": ("I", "Having alone time")},
    {"q": "You trust more:", "dimension": "SN", "a": ("S", "What you can see and touch"), "b": ("N", "Your intuition")},
    {"q": "You decide things based on:", "dimension": "TF", "a": ("T", "What makes sense"), "b": ("F", "What feels right")},
]

personality_descriptions = {
    "ENTJ": "ENTJs are natural-born leaders, driven to achieve and organize. They excel in planning and executing, often leading teams with efficiency and confidence. They are decisive and love challenges.",
    "INTJ": "INTJs are strategic thinkers, often focused on long-term goals. They prefer working alone, excelling at solving complex problems. They value intelligence and independence, sometimes coming across as reserved or distant.",
    "ENFP": "ENFPs are passionate and energetic individuals, often inspired by their own ideas and people around them. They value creativity and seek deeper emotional connections. They can be spontaneous and have a strong intuition.",
    "INFP": "INFPs are idealists with a deep sense of personal values. They care deeply about others, seeking meaningful connections. They are empathetic and value personal authenticity, often preferring to explore ideas on their own.",
    "ESTJ": "ESTJs are practical, reliable, and efficient. They are natural organizers who enjoy structure and clear expectations. They value tradition and work hard to ensure goals are met. They often take charge in group settings.",
    "ISTJ": "ISTJs are detail-oriented and methodical, relying on their logic and past experiences to make decisions. They value responsibility, tradition, and reliability, often finding comfort in routine.",
    "ESFP": "ESFPs are outgoing and spontaneous, often bringing joy and excitement to social situations. They value freedom and live in the moment, thriving in dynamic, sensory-rich environments.",
    "ISFP": "ISFPs are creative and sensitive, often finding beauty in the world around them. They are deeply in tune with their emotions and values, preferring to work quietly and independently in environments that encourage personal expression.",
    "ENTP": "ENTPs are quick-witted and inventive, constantly generating new ideas and debating various perspectives. They enjoy challenges and intellectual debates, often looking to challenge the status quo.",
    "INTP": "INTPs are analytical and deeply curious individuals. They enjoy exploring abstract ideas and theories, often preferring to analyze information before drawing conclusions. They value independence and intellectual freedom.",
    "ESFJ": "ESFJs are caring and sociable individuals, focused on creating harmony and helping others. They value tradition and community, often working to ensure that others feel comfortable and supported.",
    "ISFJ": "ISFJs are nurturing and protective, often putting the needs of others first. They value tradition, loyalty, and security, often working behind the scenes to make sure everything runs smoothly.",
    "ESTP": "ESTPs are action-oriented and energetic, thriving in fast-paced environments. They are practical and enjoy solving problems in real-time. They often take risks and are driven by the need for excitement.",
    "ISTP": "ISTPs are practical and hands-on problem solvers, known for their ability to remain calm in stressful situations. They are independent and enjoy working on projects that require technical skill.",
    "ENFJ": "ENFJs are empathetic and charismatic leaders, deeply attuned to the needs of others. They excel in fostering strong relationships and motivating others to work towards common goals.",
    "INFJ": "INFJs are deep thinkers with a strong sense of personal integrity. They are focused on creating meaningful, lasting connections and often seek to help others. They value introspection and personal growth."
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        session['answers'] = request.form
        return redirect(url_for('result'))
    return render_template('quiz.html', questions=enumerate(questions))

@app.route('/result')
def result():
    answers = session.get('answers', {})
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    for i, q in enumerate(questions):
        answer = answers.get(f"q{i}")
        if answer:
            scores[answer] += 1

    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"

    return render_template('result.html', mbti=mbti, personality_descriptions=personality_descriptions)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        print(f"Feedback from {name}: {message}")
        return redirect(url_for('thankyou', name=name))
    return render_template('feedback.html')

@app.route('/thankyou', methods=['GET'])
def thankyou():
    name = request.args.get('name')

    return render_template('thank_you_for_feedback.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)

