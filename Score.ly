\version "2.18.0"
#(set-default-paper-size "letter" 'landscape)
#(set-global-staff-size 19)

\header {
	dedication = \markup{\italic""}
	title = "Waves"
	subsubtitle = \markup{\italic{"
%name
"}}
	subtitle = " "
	composer = \markup{\column{" " "Brian Ellis" " "}}
	arranger = " " 
	tagline = \markup{\column{" " "www.brianellissound.com"}}
}

\paper{
  indent = 0\cm
  left-margin = 2\cm
  right-margin = 2\cm
  top-margin = 2\cm
  bottom-margin = 2\cm
  max-systems-per-page = 4
  ragged-last-bottom = ##f

}

\score {
	\midi {}
	\layout {}

<<
	\new Staff \absolute {
    \once \override Staff.TimeSignature #'stencil = ##f 
	\override Score.BarNumber.stencil = ##f
	\override Score.BarLine.stencil = ##f
	\time 1/1
	\clef "treble"
	\numericTimeSignature

%part1


	\revert Score.BarLine.stencil
}

	\new Staff \absolute {
    \once \override Staff.TimeSignature #'stencil = ##f 
	\override Score.BarNumber.stencil = ##f
	\override Score.BarLine.stencil = ##f
	\time 1/1
	\clef "treble"
	\numericTimeSignature

%part0


	\revert Score.BarLine.stencil
	\bar "|."}


>>
}