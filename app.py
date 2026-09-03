import os

from flask import Flask, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fourfold-local-development-key")


questions = [
    {"q": "At a party, you’re more likely to…", "a": ("E", "Move around and meet everyone"), "b": ("I", "Settle in with a few close people")},
    {"q": "When a new project lands, you want to…", "a": ("S", "Start with a method that already works"), "b": ("N", "Try an idea no one has tested yet")},
    {"q": "A difficult decision feels right when…", "a": ("T", "The reasoning holds up"), "b": ("F", "The people involved feel understood")},
    {"q": "Plans feel most useful when they…", "a": ("J", "Settle the details early"), "b": ("P", "Leave room to change course")},
    {"q": "In a group conversation, you tend to…", "a": ("E", "Think out loud and keep it moving"), "b": ("I", "Listen first and speak when it matters")},
    {"q": "What catches your attention first?", "a": ("S", "What is concrete and observable"), "b": ("N", "What it could mean or become")},
    {"q": "When tension shows up, you trust…", "a": ("T", "A fair, consistent standard"), "b": ("F", "Context, empathy, and harmony")},
    {"q": "Your best working rhythm is…", "a": ("J", "Clear milestones and a finish line"), "b": ("P", "Freedom to follow the energy")},
    {"q": "Around someone new, you usually…", "a": ("E", "Open the conversation yourself"), "b": ("I", "Wait until there’s a natural opening")},
    {"q": "You understand something best through…", "a": ("S", "Specific examples and steps"), "b": ("N", "Patterns and the bigger picture")},
    {"q": "When choices affect others, you prioritize…", "a": ("T", "Clarity and equal treatment"), "b": ("F", "Care and individual needs")},
    {"q": "Your workspace is more often…", "a": ("J", "Ordered enough to know where things are"), "b": ("P", "A little chaotic, but alive")},
    {"q": "After a long week, you recover through…", "a": ("E", "Fresh energy from other people"), "b": ("I", "Uninterrupted time to yourself")},
    {"q": "When facts are incomplete, you lean on…", "a": ("S", "What experience has already shown"), "b": ("N", "A hunch about where things connect")},
    {"q": "Your first filter for an idea is…", "a": ("T", "Does this make sense?"), "b": ("F", "Does this feel true to me?")},
]


personality_profiles = {
    "ENTJ": {"title": "The Mobilizer", "description": "You naturally turn possibilities into plans and plans into movement. You are energized by people, direct with decisions, and most comfortable when there is a clear direction forward.", "traits": ["Decisive", "Strategic", "Driven"]},
    "INTJ": {"title": "The Systems Thinker", "description": "You look for the structure beneath the surface. Independent and future-focused, you prefer thoughtful plans, capable people, and enough quiet to solve the hard part properly.", "traits": ["Independent", "Strategic", "Focused"]},
    "ENFP": {"title": "The Possibility Seeker", "description": "You notice potential everywhere—in ideas, people, and the spaces between them. Curiosity and personal meaning pull you forward more than a fixed map ever could.", "traits": ["Curious", "Expressive", "Adaptable"]},
    "INFP": {"title": "The Quiet Idealist", "description": "You carry a strong inner compass and a vivid private world. You care about authenticity, choose depth over noise, and do your best work when it connects to something meaningful.", "traits": ["Reflective", "Empathetic", "Imaginative"]},
    "ESTJ": {"title": "The Coordinator", "description": "You create order people can rely on. Practical, direct, and steady under responsibility, you prefer clear expectations and take satisfaction in making the whole system work.", "traits": ["Reliable", "Practical", "Organized"]},
    "ISTJ": {"title": "The Steady Builder", "description": "You trust preparation, evidence, and work done with care. You are dependable without needing attention for it, and you tend to strengthen whatever you commit to over time.", "traits": ["Thorough", "Grounded", "Consistent"]},
    "ESFP": {"title": "The Live Wire", "description": "You meet the present moment with warmth and full attention. You read the room quickly, bring people into the experience, and prefer real life over too much theory.", "traits": ["Warm", "Spontaneous", "Observant"]},
    "ISFP": {"title": "The Gentle Maker", "description": "You notice details others miss and respond to the world with a quiet sense of care. Freedom, beauty, and honest self-expression matter more to you than rigid expectations.", "traits": ["Sensitive", "Flexible", "Creative"]},
    "ENTP": {"title": "The Challenger", "description": "You test ideas by turning them around, taking them apart, and asking what everyone else missed. Novelty gives you energy, and constraints often look like invitations.", "traits": ["Inventive", "Quick-witted", "Exploratory"]},
    "INTP": {"title": "The Conceptualist", "description": "You are driven to understand how things actually work. You value clean logic, intellectual freedom, and the time to follow a question farther than most people would.", "traits": ["Analytical", "Original", "Curious"]},
    "ESFJ": {"title": "The Community Keeper", "description": "You notice what helps people feel included, supported, and connected. Reliability is one of the ways you show care, and shared rituals give your world texture.", "traits": ["Supportive", "Sociable", "Attentive"]},
    "ISFJ": {"title": "The Quiet Anchor", "description": "You bring careful attention and understated loyalty to the people and places you value. You remember the details, follow through, and make stability feel human.", "traits": ["Loyal", "Considerate", "Dependable"]},
    "ESTP": {"title": "The Improviser", "description": "You are at your best where something real is happening. Fast to observe and ready to respond, you would rather test an answer in motion than debate it forever.", "traits": ["Bold", "Practical", "Responsive"]},
    "ISTP": {"title": "The Troubleshooter", "description": "You stay calm long enough to see what the problem is actually asking for. Independent and hands-on, you prefer elegant fixes, useful skills, and room to move your own way.", "traits": ["Resourceful", "Calm", "Independent"]},
    "ENFJ": {"title": "The Catalyst", "description": "You read people closely and instinctively look for the direction that brings them together. You lead through encouragement, conviction, and a clear sense of shared purpose.", "traits": ["Perceptive", "Encouraging", "Purposeful"]},
    "INFJ": {"title": "The Insight Keeper", "description": "You connect subtle patterns with a deeply personal sense of purpose. Private but compassionate, you are drawn to work and relationships that can create lasting change.", "traits": ["Insightful", "Principled", "Compassionate"]},
}


dimension_copy = {
    "EI": {
        "label": "Energy", "left": ("E", "Extraversion"), "right": ("I", "Introversion"),
        "E": "You tend to find momentum through interaction and external activity.",
        "I": "You tend to restore your energy through privacy and internal reflection.",
    },
    "SN": {
        "label": "Information", "left": ("S", "Sensing"), "right": ("N", "Intuition"),
        "S": "You tend to trust concrete details, experience, and what is observable.",
        "N": "You tend to notice patterns, implications, and what could be possible.",
    },
    "TF": {
        "label": "Decisions", "left": ("T", "Thinking"), "right": ("F", "Feeling"),
        "T": "You tend to weigh decisions through logic, clarity, and consistency.",
        "F": "You tend to weigh decisions through values, context, and human impact.",
    },
    "JP": {
        "label": "Approach", "left": ("J", "Judging"), "right": ("P", "Perceiving"),
        "J": "You tend to prefer decisions, structure, and a settled direction.",
        "P": "You tend to prefer flexibility, discovery, and keeping options open.",
    },
}


def calculate_result(answers):
    scores = {letter: 0 for letter in "EISNTFJP"}

    for index, question in enumerate(questions):
        answer = answers.get(f"q{index}")
        valid_answers = {question["a"][0], question["b"][0]}
        if answer in valid_answers:
            scores[answer] += 1

    mbti = ""
    dimensions = []
    for pair in ("EI", "SN", "TF", "JP"):
        details = dimension_copy[pair]
        left_letter, left_name = details["left"]
        right_letter, right_name = details["right"]
        left_score = scores[left_letter]
        right_score = scores[right_letter]
        total = max(left_score + right_score, 1)
        selected = left_letter if left_score >= right_score else right_letter
        mbti += selected
        dimensions.append({
            "pair": pair,
            "label": details["label"],
            "selected": selected,
            "left_letter": left_letter,
            "left_name": left_name,
            "left_percent": round(left_score / total * 100),
            "right_letter": right_letter,
            "right_name": right_name,
            "right_percent": round(right_score / total * 100),
            "insight": details[selected],
        })

    return mbti, dimensions


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        session["answers"] = request.form.to_dict()
        return redirect(url_for("result"))
    return render_template("quiz.html", questions=enumerate(questions), total=len(questions))


@app.route("/result")
def result():
    answers = session.get("answers", {})
    if any(f"q{index}" not in answers for index in range(len(questions))):
        return redirect(url_for("quiz"))
    mbti, dimensions = calculate_result(answers)
    return render_template("result.html", mbti=mbti, profile=personality_profiles[mbti], dimensions=dimensions)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form["name"].strip()
        message = request.form["message"].strip()
        print(f"Feedback from {name}: {message}")
        return redirect(url_for("thankyou", name=name))
    return render_template("feedback.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thank_you_for_feedback.html", name=request.args.get("name") or "Friend")


if __name__ == "__main__":
    app.run(debug=True)
