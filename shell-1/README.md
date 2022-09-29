# shell-1

This is a (currently unnamed) command shell based on an interpreter implemented
in Rust. It aims to take the untyped "all data is a string" semantics used in
scripting languages like Bash to the most extreme degree possible in a
practical shell programming interface; specifically, I was curious whether the
unusual stream-based semantics present in many Unix scripting tools could be
made scalable by better handling edge cases and providing developers with a
more consistent mental model that was less reliant on unwieldy clusters of
quotes and escape characters. This project is nevertheless mainly for fun, but
it is possible that it will eventually become stable enough to have (limited)
applications in real-world settings.
