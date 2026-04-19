Part 3, Task 4:
26. Why does the request use a client-generated id rather than a server-generated one? What problem does this solve in distributed systems?

The request uses a client-generated id rather than a server-generated one because it allows 
the client to identify and track its requests across retries and multiple services. With a
server-generated ID, in the event of a network failure or timeout, the client may never be
able to refer to a request made during that event, as it never received an ID from the server.
What this solves in distributed systems is the issue of a double execution of a retried task.
The client could retry a task after a failure with their client-generated ID, and the server, 
which has already processed it but failed to return it, can return it without doing work again.


27. The status.state can be 'working'. Under what circumstances would a server return this state in a non-streaming call, and how should a client react?

The server returning status.state = 'working' in a non-streaming call can mean that the client's 
request has been accepted by the server, but it has not been completed yet. The client should 
react by repeatedly waiting for a moment and retrying until the state changes to a conclusive
state.


28. What is the purpose of the sessionId field? Give a concrete example of two related tasks that should share a session.

The purpose of the sessionId field is to group related tasks into a shared conversational 
context, allowing for context persistence and multi-step workflows. For instance, a  
requested task can be "Recommend some action movies to watch," with the follow up task being
"Now recommend some that a child can watch." Both of these tasks would share the same
sessionId, allowing the server to maintain and consider task 1 as context while processing
task 2. As a result, the server understands that task 2 is a follow-up to task 1, so as it
processes task 2, it understands that it's still recommending action movies, but now for a
child to safely watch.


29. The parts array supports types text, file, and data. Describe a realistic multi-agent workflow where all three part types appear in a single conversation.

One possible example of a multi-agent workflow in which part types text, file, and data appear in 
the same conversation could be in a research report generation agent. In step 1, the user prompts
agent A with a PDF upload and text "Summarize this document and extract key statistics." In step
2, agent A contacts agent B and provides it the prompt it was received, from which agent B will
generate structured data of the document. Then, in step 3, agent B will contact agent C,
providing it with the structured data and text from agent A, from which agent C will generate a
report. Lastly, agent C will then send the results to agent A, who then sends the report file
and summary to the user.


Part 4, Task 5:
37. In report.md Section 4, describe: (a) what the --allow-unauthenticated flag does and its security implications, (b) how Cloud Run scales to zero and what cold start latency means for A2A clients.

a.) The flag --allow-unauthenticated grants the Cloud Run Invoker IAM role to the allUsers member type. This makes the service publicly accessible to any user, without authentication or identification, over HTTPS, allowing them to call our endpoints directly. What this implies for security is an increased attack surface, as there may be unauthorized usage of endpoints, which could return sensitive information, and potential abuse through spam or scraping. Untrusted traffic may additionally increase costs, as they generate billable requests.

b.) When there's no traffic, Cloud Run automatically scales to zero by reducing the number of running instances to 0, eliminating idle compute cost. What cold start latency could mean for A2A clients is a noticeable delay when making a request, as Cloud Run has to boot up a new container instance, and that startup time for the container may add the latency. 