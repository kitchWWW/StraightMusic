import datetime
import sys
import copy
import random

timestamp = '' #sys.argv[1]
dedication = 'Brian' # sys.argv[2]



overallSeconds = random.randint(8*60,12*60)
timeSlots = range(overallSeconds)

maxLength = 30
minLength = 10
minWaitForFirst = 25
minSpacer = 10
howManyPhasesBeyondFirstTwo = random.randint(10,20)

mallets = ['cardboard','soft','medium','hard']

howManyOctaves = 4

transitions = [0]*(howManyOctaves-1)


goodToGo = False
while goodToGo == False:
	transitions = sorted(random.sample(timeSlots,howManyOctaves-1))
	#print transitions
	goodToGo = True
	failureReasons = []
	if transitions[0] < overallSeconds/howManyOctaves:
		goodToGo = False
		failureReasons.append('start too soon')
	if transitions[0] > overallSeconds/2.5:
		goodToGo = False
		failureReasons.append('start too late')
	if transitions[len(transitions)-1] > overallSeconds - (overallSeconds/howManyOctaves+5):
		goodToGo = False
		failureReasons.append('end too late')
	if transitions[len(transitions)-1] < overallSeconds - (overallSeconds/2.5):
		goodToGo = False
		failureReasons.append('end too early')
	for i in range(howManyOctaves-2):
		if transitions[i+1] - transitions[i] < 1.5*60:
			goodToGo = False
			failureReasons.append('too short middle')
	print failureReasons

print transitions
toAdd = []
for i in range(len(transitions)-1):
	toAdd.append(random.randint(transitions[i]+maxLength,transitions[i+1]-maxLength))
transitions.extend(toAdd)
transitions = sorted(transitions)
print transitions

# insert phases
playing = 0
assignments = []
for i in range(overallSeconds):
	assignments.append([0,0])

for i in range(overallSeconds):
	if i in transitions:
		playing = (playing+1) % 2
	assignments[i][playing] = 'pulse'


howManyToDelete = random.randint(0,len(transitions)-1)
for i in range(howManyToDelete):
	del transitions[random.randint(0,len(transitions)-1)]

transitionActions = []
for transitionLocation in transitions:
	transitionActions.append(transitionLocation-random.randint(7,15))
	transitionActions.append(transitionLocation+random.randint(7,15))

for i in range(random.randint(10,30)):
	assignments[i][0] = 'fade'

print transitionActions
inTransition = False
for i in range(overallSeconds):
	if i in transitionActions:
		inTransition = not inTransition
	if inTransition:
		assignments[i][0] = 'fade'
		assignments[i][1] = 'fade'



wavesAdded = 0
targetWaves = random.randint(7,13)
triesWithoutSuccess = 0
while triesWithoutSuccess < 4000:
	triesWithoutSuccess += 1
	print triesWithoutSuccess
	addLocation = random.randint(minWaitForFirst,overallSeconds-maxLength-minSpacer)
	side = random.randint(0,1)
	if assignments[addLocation][0] == 0:
		side = 0
	if assignments[addLocation][1] == 0:
		side = 1
	proposedLength = random.randint(minLength,maxLength)
	allowable = [0,'pulse']
	orig = assignments[addLocation][side]
	if orig not in allowable:
		continue
	canAdd=True
	for i in range(addLocation-minSpacer,addLocation+proposedLength+minSpacer):
		if assignments[i][side] != orig:
			canAdd = False
		if assignments[i][(side+1) % 2] not in allowable:
			canAdd = False
	if canAdd == False:
		continue
	for i in range(addLocation,addLocation+proposedLength):
		assignments[i][side] = 'wave'
	wavesAdded += 1
	triesWithoutSuccess = 0


print "going!"
malletAssignments = []
oldAssignment = [random.randint(0,1),-1]
for i in range(overallSeconds):
	newAssignment = [oldAssignment[0],oldAssignment[1]]
	for p in range(2):
		if assignments[i][p] == 0:
			newAssignment[p] = -1
	if i > 1:
		for p in range(2):
			if assignments[i-1][p] == 0 and assignments[i][p] != 0:
				if assignments[i] == 'wave':
					newAssignment[p] = random.randint(oldAssignment[(p+1)%2]+1,len(mallets)-1)
				else:
					newAssignment[p] = random.randint(0,len(mallets)-2)
					if newAssignment[p] == newAssignment[(p+1)%2]:
						newAssignment[p] = newAssignment[p]+1
	print newAssignment
	malletAssignments.append(newAssignment)
	oldAssignment = newAssignment

print malletAssignments


octaveAssignments = [0]*overallSeconds
base = 0
top = 1
for i in range(overallSeconds):
	if assignments[i][0] == 'fade' or assignments[i][0] == 'pulse':
		if i > 1:
			if assignments[i-1][0] == 0:
				base += 1
			if base == top and assignments[i][1] ==0:
				top+=1
	octaveAssignments[i] = [base, top]


print octaveAssignments








instructions = []
for i in range(len(assignments)):
	pa = str(assignments[i][0]) 
	if malletAssignments[i][0] != -1:
		pa = pa +'-'+str(mallets[malletAssignments[i][0]])
		pa=pa+'-f'+str(octaveAssignments[i][0])
	pa = pa + ' '*(18-len(pa))

	pb = str(assignments[i][1])
	if malletAssignments[i][1] != -1:
		pb = pb+ '-'+str(mallets[malletAssignments[i][1]])
		pb=pb+'-f'+str(octaveAssignments[i][1])
	pb = pb + ' '*(18-len(pb))


	mins = str(int(i/60))
	mins = '0'*(1-len(mins))+mins
	secs = str(int(i%60))
	secs = '0'*(2-len(secs))+secs

	time = mins+':'+secs

	instructions.append([time,pa,pb,i])

	print time+' = '+ pa +'| '+pb

i = 1
while i < len(instructions)-1:
	if instructions[i][1] == instructions[i-1][1] and instructions[i][2] == instructions[i-1][2]:
		del instructions[i]
		i-=1
	i+=1

parts = [[],[]]
prevDynamics = ''
tiedFromPrev = ''
dynamicsFromPrev = ''
needsBreak = False
sinceBreak = 0
for p in range(2):
	for i in range(len(instructions)):
		timeIndex = instructions[i][3]
		time = ''
		if p == 1:
			time = '^"'+instructions[i][0]+'"'
			print time
		toWrite = ''
		note = ''
		dynamics = ''
		nextTie = ''
		nextDynamics = ''
		if assignments[timeIndex][p] != 0:
			note = 'f'+"'"*int(octaveAssignments[timeIndex][p]) +'1:32'
			nextTie = '~'
		else:
			note = 's1'
			nextTie = ''
			tiedFromPrev = ''
		print instructions[i-1][1+p]
		prevTimeIndex = instructions[i-1][3]
		if assignments[timeIndex][p] == 'fade':
			if assignments[prevTimeIndex][p] == 0:
				dynamics = '\\<'
				nextDynamics = '\\!'
			else:
				dynamics = '\\>'
				nextDynamics = '\\!'

		partForInstruction = ''
		if assignments[timeIndex][p] == 'wave':
			partForInstruction = tiedFromPrev + note +' \\< '+time+' ~'+ note+' \\!\\>'
			nextDynamics = '\\!'
		elif assignments[timeIndex][(p+1)%2] == 'wave':
			partForInstruction = tiedFromPrev + ' ' +note+time+ ((' ~' + note))
			nextTie = '~'
		else:
			partForInstruction = tiedFromPrev+note+dynamicsFromPrev+dynamics+time
		sinceBreak += 1
		if sinceBreak > 7:
			needsBreak = True
		if nextTie == '' and needsBreak == True and p == 0:
			partForInstruction += "\n\\pageBreak\n "
			needsBreak = False
			sinceBreak = 0
		parts[p].append(partForInstruction)
		tiedFromPrev = nextTie
		dynamicsFromPrev = nextDynamics


for p in parts:
	print "part:"
	print '   '.join(p)

fd = open("Score.ly",'r')
out = open("out/out.ly",'w')
for l in fd:
	if 'part' in l:
		index = int(l[5:].strip())
		l = '    '.join(parts[index])
	out.write(l)

out.close()
fd.close()		




# for i in range(len(instructions)-1,1,-1):
# 	if instructions[i][1] == instructions[i-1][1] and instructions[i][1].strip() != '0':
# 		instructions[i][1] = '(cont.)           '
# 	if instructions[i][2] == instructions[i-1][2] and instructions[i][2].strip() != '0':
# 		instructions[i][2] = '(cont.)           '
	
print "Wall-clock Time (mm:ss) & Lefthand & Righthand \\\\ \\hline"
for i in range(len(instructions)):
	print ' & '.join(instructions[i][:3]) +" \\\\ \\hline"

indexFirst = random.randint(minWaitForFirst, transitions[0] - maxLength)
indexFirstElectronic = random.randint(minWaitForFirst, transitions[0] - maxLength)



