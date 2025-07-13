(define (domain wumpus)

(:requirements :strips :typing)

(:types location object
    agent pushable wampus arrow fireworks pit - object
    crate halfcrate - pushable
)

(:predicates (at ?o - object ?l - location) (valid ?l - location) (adjacente ?l1 - location ?l2 - location) (finish)
(adjacentw ?l1 - location ?l2 - location) (adjacents ?l1 - location ?l2 - location) (adjacentn ?l1 - location ?l2 - location)
(target ?l - location) (hasArrows ?a - agent ?n - arrow) (hasFireworks ?a - agent ?f - fireworks) (halfFilled ?l - location) (emptypit ?l - location) (blocked ?l - location) (fullyfilled ?l - location)

)


(:action moveEast
    :parameters (?o - agent ?l1 - location ?l2 - location)
    :precondition (and (at ?o ?l1) (adjacente ?l1 ?l2) (valid ?l2))
    :effect (and (at ?o ?l2) (not (at ?o ?l1)) (valid ?l1))
)

(:action moveWest
    :parameters (?o - agent ?l1 - location ?l2 - location)
    :precondition (and (at ?o ?l1) (adjacentw ?l1 ?l2) (valid ?l2))
    :effect (and (at ?o ?l2) (not (at ?o ?l1))(valid ?l1))
)

(:action moveNorth
    :parameters (?o - agent ?l1 - location ?l2 - location)
    :precondition (and (at ?o ?l1) (adjacentn ?l1 ?l2) (valid ?l2))
    :effect (and (at ?o ?l2) (not (at ?o ?l1)) (valid ?l1))
)

(:action moveSouth
    :parameters (?o - agent ?l1 - location ?l2 - location)
    :precondition (and (at ?o ?l1) (adjacents ?l1 ?l2) (valid ?l2))
    :effect (and (at ?o ?l2) (not (at ?o ?l1)) (valid ?l1))
)

(:action lastMove
   :parameters (?o - agent ?loc - location)
   :precondition (and (at ?o ?loc) (target ?loc))
   :effect (and (finish))
)

(:action pushSouth
    :parameters (?o1 - agent ?o2 - pushable ?h - halfcrate ?p - pit ?c - crate ?l1 - location ?l2 - location ?l3 - location)
    :precondition (and (at ?o1 ?l1) (adjacents ?l1 ?l2) (at ?o2 ?l2) (not (at ?p ?l2)) (adjacents ?l2 ?l3) (or (valid ?l3) (and (at ?p ?l3) (not (blocked ?l3)))))
    :effect (and (when (valid ?l3) (and (at ?o1 ?l2) (at ?o2 ?l3) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (valid ?l3)) (valid ?l1)))
    (when (and (at ?p ?l3) (emptypit ?l3)) (and (valid ?l1) (not (emptypit ?l3)) (at ?o1 ?l2) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (when (at ?h ?l2) (and (at ?o2 ?l3) (halfFilled ?l3))) (when (at ?c ?l2) (and (fullyfilled ?l3) (not (at ?p ?l3)) (not (at ?c ?l2)) (not (at ?o2 ?l3)) (valid ?l3)))))
    (when (and (at ?p ?l3) (halfFilled ?l3)) (and (valid ?l1) (not (halfFilled ?l3)) (at ?o1 ?l2) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (when (at ?h ?l2) (and (fullyfilled ?l3) (not (at ?p ?l3)) (not (at ?h ?l3)) (not (at ?o2 ?l3)) (valid ?l3))) (when (at ?c ?l2) (and (at ?o2 ?l3) (blocked ?l3)))))
    (when (and (at ?p ?l3) (fullyFilled ?l3) (at ?h ?l2)) (and (valid ?l1) (not (fullyFilled ?l3)) (blocked ?l3) (at ?o1 ?l2) (at ?o2 ?l3) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (blocked ?l3)))
    ) 
)

(:action pushEast
    :parameters (?o1 - agent ?o2 - pushable ?h - halfcrate ?p - pit ?c - crate ?l1 - location ?l2 - location ?l3 - location)
    :precondition (and (at ?o1 ?l1) (adjacente ?l1 ?l2) (at ?o2 ?l2) (not (at ?p ?l2)) (adjacente ?l2 ?l3) (or (valid ?l3) (and (at ?p ?l3) (not (blocked ?l3)))))
    :effect (and (when (valid ?l3) (and (at ?o1 ?l2) (at ?o2 ?l3) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (valid ?l3)) (valid ?l1)))
    (when (and (at ?p ?l3) (emptypit ?l3)) (and (valid ?l1) (not (emptypit ?l3)) (at ?o1 ?l2) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (when (at ?h ?l2) (and (at ?o2 ?l3) (halfFilled ?l3))) (when (at ?c ?l2) (and (fullyfilled ?l3) (not (at ?p ?l3)) (not (at ?c ?l2)) (not (at ?o2 ?l3)) (valid ?l3)))))
    (when (and (at ?p ?l3) (halfFilled ?l3)) (and (valid ?l1) (not (halfFilled ?l3)) (at ?o1 ?l2) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (when (at ?h ?l2) (and (fullyfilled ?l3) (not (at ?p ?l3)) (not (at ?h ?l3)) (not (at ?o2 ?l3)) (valid ?l3))) (when (at ?c ?l2) (and (at ?o2 ?l3) (blocked ?l3)))))
    (when (and (at ?p ?l3) (fullyFilled ?l3) (at ?h ?l2)) (and (valid ?l1) (not (fullyFilled ?l3)) (blocked ?l3) (at ?o1 ?l2) (at ?o2 ?l3) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (blocked ?l3)))
    ) 
)

(:action pushWest
    :parameters (?o1 - agent ?o2 - pushable ?h - halfcrate ?p - pit ?c - crate ?l1 - location ?l2 - location ?l3 - location)
    :precondition (and (at ?o1 ?l1) (adjacentw ?l1 ?l2) (not (at ?p ?l2)) (at ?o2 ?l2) (adjacentw ?l2 ?l3) (or (valid ?l3) (and (at ?p ?l3) (not (blocked ?l3)))))
    :effect (and (when (valid ?l3) (and (at ?o1 ?l2) (at ?o2 ?l3) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (valid ?l3)) (valid ?l1)))
    (when (and (at ?p ?l3) (emptypit ?l3)) (and (valid ?l1) (not (emptypit ?l3)) (at ?o1 ?l2) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (when (at ?h ?l2) (and (at ?o2 ?l3) (halfFilled ?l3))) (when (at ?c ?l2) (and (fullyfilled ?l3) (not (at ?p ?l3)) (not (at ?c ?l2)) (not (at ?o2 ?l3)) (valid ?l3)))))
    (when (and (at ?p ?l3) (halfFilled ?l3)) (and (valid ?l1) (not (halfFilled ?l3)) (at ?o1 ?l2) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (when (at ?h ?l2) (and (fullyfilled ?l3) (not (at ?p ?l3)) (not (at ?h ?l3)) (not (at ?o2 ?l3)) (valid ?l3))) (when (at ?c ?l2) (and (at ?o2 ?l3) (blocked ?l3)))))
    (when (and (at ?p ?l3) (fullyFilled ?l3) (at ?h ?l2)) (and (valid ?l1) (not (fullyFilled ?l3)) (blocked ?l3) (at ?o1 ?l2) (at ?o2 ?l3) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (blocked ?l3)))
    ) 
)

(:action pushNorth
    :parameters (?o1 - agent ?o2 - pushable ?h - halfcrate ?p - pit ?c - crate ?l1 - location ?l2 - location ?l3 - location)
    :precondition (and (at ?o1 ?l1)  (adjacentn ?l1 ?l2) (at ?o2 ?l2) (not (at ?p ?l2)) (adjacentn ?l2 ?l3) (or (valid ?l3) (and (at ?p ?l3) (not (blocked ?l3)))))
    :effect (and (when (valid ?l3) (and (at ?o1 ?l2) (at ?o2 ?l3) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (valid ?l3)) (valid ?l1)))
    (when (and (at ?p ?l3) (emptypit ?l3)) (and (valid ?l1) (not (emptypit ?l3)) (at ?o1 ?l2) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (when (at ?h ?l2) (and (at ?o2 ?l3) (halfFilled ?l3))) (when (at ?c ?l2) (and (fullyfilled ?l3) (not (at ?p ?l3)) (not (at ?c ?l2)) (not (at ?o2 ?l3)) (valid ?l3)))))
    (when (and (at ?p ?l3) (halfFilled ?l3)) (and (valid ?l1) (not (halfFilled ?l3)) (at ?o1 ?l2) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (when (at ?h ?l2) (and (fullyfilled ?l3) (not (at ?p ?l3)) (not (at ?h ?l3)) (not (at ?o2 ?l3)) (valid ?l3))) (when (at ?c ?l2) (and (at ?o2 ?l3) (blocked ?l3)))))
    (when (and (at ?p ?l3) (fullyFilled ?l3) (at ?h ?l2)) (and (valid ?l1) (not (fullyFilled ?l3)) (blocked ?l3) (at ?o1 ?l2) (at ?o2 ?l3) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (blocked ?l3)))
    ) 
)

(:action pickUpArrow
    :parameters (?o - agent ?l - location ?a - arrow)
    :precondition (and (at ?o ?l) (at ?a ?l))
    :effect (and (hasArrows ?o ?a) (not (at ?a ?l)) )
)

(:action shotNorth
    :parameters (?o - agent ?l1 - location ?l2 - location ?a - arrow ?w - wampus)
    :precondition (and (at ?o ?l1) (adjacentn ?l1 ?l2) (at ?w ?l2) (hasArrows ?o ?a))
    :effect (and (not (at ?w ?l2)) (valid ?l2) (not (hasArrows ?o ?a)))
)

(:action shotSouth
    :parameters (?o - agent ?l1 - location ?l2 - location ?a - arrow ?w - wampus)
    :precondition (and (at ?o ?l1) (adjacents ?l1 ?l2) (at ?w ?l2) (hasArrows ?o ?a))
    :effect (and (not (at ?w ?l2)) (valid ?l2) (not (hasArrows ?o ?a)))
)

(:action shotEast
    :parameters (?o - agent ?l1 - location ?l2 - location ?a - arrow ?w - wampus)
    :precondition (and (at ?o ?l1) (adjacente ?l1 ?l2) (at ?w ?l2) (hasArrows ?o ?a))
    :effect (and (not (at ?w ?l2)) (valid ?l2) (not (hasArrows ?o ?a)))
)

(:action shotWest
    :parameters (?o - agent ?l1 - location ?l2 - location ?a - arrow ?w - wampus)
    :precondition (and (at ?o ?l1) (adjacentw ?l1 ?l2) (at ?w ?l2) (hasArrows ?o ?a))
    :effect (and (not (at ?w ?l2)) (valid ?l2) (not (hasArrows ?o ?a)))
)

(:action pickUpFireworks
    :parameters (?o - agent ?l - location ?a - fireworks)
    :precondition (and (at ?o ?l) (at ?a ?l))
    :effect (and (hasFireworks ?o ?a) (not (at ?a ?l)) )
)

(:action scareNorth
    :parameters (?o - agent ?l1 - location ?l2 - location ?l3 - location ?w - wampus ?f - fireworks)
    :precondition (and (at ?o ?l1) (adjacentn ?l1 ?l2) (adjacentn ?l2 ?l3) (not (blocked ?l3)) (valid ?l3) (at ?w ?l2) (hasFireworks ?o ?f))
    :effect (and (not (valid ?l3)) (valid ?l2) (not (at ?w ?l2)) (at ?w ?l3) (not (hasFireworks ?o ?f)))
)

(:action scareSouth
    :parameters (?o - agent ?l1 - location ?l2 - location ?l3 - location ?w - wampus ?f - fireworks)
    :precondition (and (at ?o ?l1) (adjacents ?l1 ?l2) (adjacents ?l2 ?l3) (not (blocked ?l3)) (valid ?l3) (at ?w ?l2) (hasFireworks ?o ?f))
    :effect (and (not (valid ?l3)) (valid ?l2) (not (at ?w ?l2)) (at ?w ?l3) (not (hasFireworks ?o ?f)))
)

(:action scareWest
    :parameters (?o - agent ?l1 - location ?l2 - location ?l3 - location ?w - wampus ?f - fireworks)
    :precondition (and (at ?o ?l1) (adjacentw ?l1 ?l2) (adjacentw ?l2 ?l3) (not (blocked ?l3)) (valid ?l3) (at ?w ?l2) (hasFireworks ?o ?f))
    :effect (and (not (valid ?l3)) (valid ?l2) (not (at ?w ?l2)) (at ?w ?l3) (not (hasFireworks ?o ?f)))
)

(:action scareEast
    :parameters (?o - agent ?l1 - location ?l2 - location ?l3 - location ?w - wampus ?f - fireworks)
    :precondition (and (at ?o ?l1) (adjacente ?l1 ?l2) (adjacente ?l2 ?l3) (not (blocked ?l3)) (valid ?l3) (at ?w ?l2) (hasFireworks ?o ?f))
    :effect (and (not (valid ?l3)) (valid ?l2) (not (at ?w ?l2)) (at ?w ?l3) (not (hasFireworks ?o ?f)))
)

(:action pushHalfcrateNorth
    :parameters (?o1 - agent ?o2 - halfcrate ?o3 - halfcrate ?p - pit ?l1 - location ?l2 - location ?l3 - location ?l4 - location)
    :precondition (and (at ?o1 ?l1) (at ?o2 ?l2) (not (at ?p ?l2)) (at ?o3 ?l3) (or (valid ?l4) (and (at ?p ?l4) (not (blocked ?l4)))) (adjacentn ?l1 ?l2) (adjacentn ?l2 ?l3) (adjacentn ?l3 ?l4))
    :effect (and (when (valid ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (valid ?l4))))
    (when (emptypit ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (emptypit ?l4)) (halfFilled ?l4)))
    (when (halfFilled ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (halfFilled ?l4)) (fullyfilled ?l4) (valid ?l4)))
    (when (fullyfilled ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (blocked ?l4)))
)
)
(:action pushHalfcrateSouth
    :parameters (?o1 - agent ?o2 - halfcrate ?o3 - halfcrate ?p - pit ?l1 - location ?l2 - location ?l3 - location ?l4 - location)
    :precondition (and (at ?o1 ?l1) (at ?o2 ?l2) (not (at ?p ?l2)) (at ?o3 ?l3) (or (valid ?l4) (and (at ?p ?l4) (not (blocked ?l4)))) (adjacents ?l1 ?l2) (adjacents ?l2 ?l3) (adjacents ?l3 ?l4))
    :effect (and (when (valid ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (valid ?l4))))
    (when (emptypit ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (emptypit ?l4)) (halfFilled ?l4)))
    (when (halfFilled ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (halfFilled ?l4)) (fullyfilled ?l4) (valid ?l4)))
    (when (fullyfilled ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (blocked ?l4)))
)
)

(:action pushHalfcrateEast
    :parameters (?o1 - agent ?o2 - halfcrate ?o3 - halfcrate ?p - pit ?l1 - location ?l2 - location ?l3 - location ?l4 - location)
    :precondition (and (at ?o1 ?l1) (at ?o2 ?l2) (not (at ?p ?l2)) (at ?o3 ?l3) (or (valid ?l4) (and (at ?p ?l4) (not (blocked ?l4)))) (adjacente ?l1 ?l2) (adjacente ?l2 ?l3) (adjacente ?l3 ?l4))
    :effect (and (when (valid ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (valid ?l4))))
    (when (emptypit ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (emptypit ?l4)) (halfFilled ?l4)))
    (when (halfFilled ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (halfFilled ?l4)) (fullyfilled ?l4) (valid ?l4)))
    (when (fullyfilled ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (blocked ?l4))))
)

(:action pushHalfcrateWest
    :parameters (?o1 - agent ?o2 - halfcrate ?o3 - halfcrate ?p - pit ?l1 - location ?l2 - location ?l3 - location ?l4 - location)
    :precondition (and (at ?o1 ?l1) (at ?o2 ?l2) (not (at ?p ?l2)) (at ?o3 ?l3) (or (valid ?l4) (and (at ?p ?l4) (not (blocked ?l4)))) (adjacentw ?l1 ?l2) (adjacentw ?l2 ?l3) (adjacentw ?l3 ?l4))
    :effect (and (when (valid ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (valid ?l4))))
    (when (emptypit ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (emptypit ?l4)) (halfFilled ?l4)))
    (when (halfFilled ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (not (halfFilled ?l4)) (fullyfilled ?l4) (valid ?l4)))
    (when (fullyfilled ?l4) (and (at ?o1 ?l2) (at ?o2 ?l3) (at ?o3 ?l4) (valid ?l1) (not (at ?o1 ?l1)) (not (at ?o2 ?l2)) (not (at ?o3 ?l3)) (blocked ?l4)))
)
)

)