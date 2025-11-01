*Zero-Shot Prompts:*

1. 	A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?
	*Expected Answer: $0.10*

2. 	Q: Alice is older than Bob. Bob is older than Charlie. Who is the youngest?	
	*Charlie*

3.	Q: Classify the following review as Positive or Negative:
	"This laptop crashes constantly and I regret buying it."
	*Expected Answer: Negative*

*Few-Shot Prompts:*

1. 	Q: A pen and a pencil cost $0.30 in total. The pen costs $0.20 more than the pencil.
	A: Let pencil = x. Then pen = x + 0.20. So x + (x+0.20) = 0.30 → 2x + 0.20 = 0.30 → 2x = 0.10 → x = $0.05.

	Q: A mug and a coaster cost $2.40 in total. The mug costs $1.20 more than the coaster.
	A: Let coaster = x. Then mug = x + 1.20. So x + (x+1.20) = 2.40 → 2x + 1.20 = 2.40 → 2x = 1.20 → x = $0.60.

	Q: A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?
	*Expected Answer: $0.05*

2. 	Q: I’m tall when I’m young, and I’m short when I’m old. What am I?
	A: A Candle

	Q: The more of me you take, the more you leave behind. What am I?
	A: Footsteps

	Q: I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?
	*Expected Answer: An Echo*

3.	Q: Review: "I loved the taste of the pizza."
	A: Positive

	Q: Review: "The waiter ignored us the whole time."
	A: Negative

	Q: Review: "This laptop crashes constantly and I regret buying it."
	*Expected Answer: Negative*

*Chain-of-Thought (CoT) Prompts:*

1. 	Q: A notebook and a pen cost $1.50 in total. The notebook costs $0.90 more than the pen.
	Step 1: Let pen = x → notebook = x + 0.90
	Step 2: x + (x + 0.90) = 1.50 → 2x + 0.90 = 1.50 → 2x = 0.60 → x = $0.30
	A: $0.30

	Q: A bat and a ball cost $1.10. The bat costs $1.00 more than the ball.
	(Show steps like above and then give final answer.)


*Expected Answer: *
	*Step 1: Let the ball cost x dollars. Then the bat costs x + 1.00.*
	*Step 2: Total = x + (x + 1.00) = 1.10 → 2x + 1.00 = 1.10 → 2x = 0.10 → x = 0.05.*
	*Final answer: $0.05.*


2. 	Solve this puzzle step by step.

	Puzzle: Alice is older than Bob. Bob is older than Charlie. Who is the youngest?

	Answer (explain reasoning):
	
*Expected Answer:*
	Step 1 — Translate statements into relations:
	"Alice is older than Bob" ⇒ A>B.
	"Bob is older than Charlie" ⇒ B>C.

	Step 2 — Use transitivity of “older than”:
	From A>B and B>C we get A>B>C.

	Step 3 — Read the ordering from oldest to youngest:
	Alice, then Bob, then Charlie.

	Answer: Charlie is the youngest.


3. 	Q: Review: "I loved the taste of the pizza."
	Step 1: Identify keywords → "loved" (positive)
	Step 2: Overall sentiment = Positive
	A: Positive

	Q: Review: "The waiter ignored us the whole time."
	Step 1: Identify keywords → "ignored" (negative)
	Step 2: Overall sentiment = Negative
	A: Negative

	Q: Review: "This laptop crashes constantly and I regret buying it."
	(Show the same step-by-step identification and then give the final label.)

*Expected Answer:*
	*Step 1: Identify keywords → "crashes constantly", "regret buying"*
	*Step 2: Both express dissatisfaction and frustration*
	*Step 3: Therefore, sentiment = Negative*
	*A: Negative*