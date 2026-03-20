size(1200, 1200)

# import class
graph =  ximport("graph")

# create graph
g = graph.create(iterations=1000, distance=1.4)

# STYLES
#s = g.styles.create("owen")
#s.fill = color(1, 0, 0.25, 0.75)
#s.background = color(1, 0, 0.25, 0.75)
#g.style = "owen"

g.styles.default.fontsize = 10
g.styles.default.background = color(0, 0, 0)
g.styles.default.fill = color(0.5, 0.5, 0.5, 0)



# center
#g.add_node("home", style="owen")
#g.add_node("site/contact", category="library")






g.add_node("General Atomics Aeronautical Systems Inc.")
g.add_edge("General Atomics Aeronautical Systems Inc.","General Atomics Aeronautical Systems News")
g.add_edge("General Atomics Aeronautical Systems Inc.","Lynx SAR/GTMI Radar System")
g.add_edge("General Atomics Aeronautical Systems Inc.","General Atomics Aeronautical Systems Inc.")
g.add_edge("General Atomics Aeronautical Systems Inc.","Resources")
g.add_edge("General Atomics Aeronautical Systems Inc.","General Atomics Aeronautical Systems News")
g.add_edge("General Atomics Aeronautical Systems Inc.","Contact Information")
g.add_edge("General Atomics Aeronautical Systems Inc.","GA-ASI Image Library")
g.add_edge("General Atomics Aeronautical Systems Inc.","Careers at General Atomics Aeronautical Systems")
g.add_edge("General Atomics Aeronautical Systems Inc.","General Atomics Aeronautical Systems News")
g.add_edge("General Atomics Aeronautical Systems Inc.","Capabilities")
g.add_edge("General Atomics Aeronautical Systems Inc.","Products & Services")
g.add_edge("General Atomics Aeronautical Systems Inc.","General Atomics Aeronautical Systems Industry Milestones")
g.add_edge("General Atomics Aeronautical Systems Inc.","General Atomics Aeronautical Systems Inc.")
g.add_node("General Atomics Aeronautical Systems Industry Milestones")
g.add_edge("General Atomics Aeronautical Systems Industry Milestones","GA-ASI Image Library")
g.add_node("Products & Services")
g.add_edge("Products & Services","I-GNAT")
g.add_edge("Products & Services","I-GNAT ER/Sky Warrior Alpha ")
g.add_edge("Products & Services","Predator")
g.add_edge("Products & Services","Sky Warrior")
g.add_edge("Products & Services","Predator B")
g.add_edge("Products & Services","Lynx Product Family")
g.add_edge("Products & Services","CLAW Sensor Control")
g.add_edge("Products & Services","Athena RF Tag")
g.add_edge("Products & Services","Ground Control Stations")
g.add_edge("Products & Services","Rover")
g.add_edge("Products & Services","Ground Control Stations")
g.add_edge("Products & Services","Ground Control Stations")
g.add_edge("Products & Services","Government Laser Systems")
g.add_node("General Atomics Aeronautical Systems News")
g.add_edge("General Atomics Aeronautical Systems News","Accolades")
g.add_node("Careers at General Atomics Aeronautical Systems")
g.add_edge("Careers at General Atomics Aeronautical Systems","Careers at General Atomics Aeronautical Systems")
g.add_edge("Careers at General Atomics Aeronautical Systems","General Atomics Aeronautical Systems Inc.")
g.add_edge("Careers at General Atomics Aeronautical Systems","Careers at General Atomics Aeronautical Systems")
g.add_edge("Careers at General Atomics Aeronautical Systems","Careers at General Atomics Aeronautical Systems")
g.add_node("GA-ASI Image Library")
g.add_edge("GA-ASI Image Library","ALTAIR Image Library")
g.add_edge("GA-ASI Image Library","ALTUS Image Library")
g.add_edge("GA-ASI Image Library","Company Photos")
g.add_edge("GA-ASI Image Library","GNAT Image Library")
g.add_edge("GA-ASI Image Library","Ground Control Stations Image Library")
g.add_edge("GA-ASI Image Library","Lynx Product Family Image Library")
g.add_edge("GA-ASI Image Library","Other Air Vehicles Image Library")
g.add_edge("GA-ASI Image Library","Predator Image Library")
g.add_edge("GA-ASI Image Library","Predator B Image Library")
g.add_edge("GA-ASI Image Library","Prowler II Image Library")
g.add_edge("GA-ASI Image Library","Related Photos Image Library")
g.add_node("General Atomics Aeronautical Systems News")
g.add_edge("General Atomics Aeronautical Systems News","Fleet Comparison")
g.add_node("Government Laser Systems")
g.add_edge("Government Laser Systems","Government Laser Systems")
g.add_edge("Government Laser Systems","Government Laser Systems")



g.prune(depth=0)    # remove orphans
g.solve()           # calculate a good layout
#g.styles.apply()   # apply default styles
g.draw(
    directed=False,
    traffic=None
)


print( "___GRAPH DRAWN_________________________________________________________________________________" )
