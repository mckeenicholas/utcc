export interface Competition {
	name: string;
	date: string;
}

export interface CompetitionListItem {
	id: number;
	name: string;
	date: string;
}

export interface CompetitionList {
	competitions: CompetitionListItem[];
}

export type WCAEvent = keyof typeof eventNames;

export const eventNames = {
	'333': '3x3x3 Cube',
	'222': '2x2x2 Cube',
	'444': '4x4x4 Cube',
	'555': '5x5x5 Cube',
	'666': '6x6x6 Cube',
	'777': '7x7x7 Cube',
	'333bf': '3x3x3 Blindfolded',
	'333fm': '3x3x3 Fewest Moves',
	'333oh': '3x3x3 One-Handed',
	minx: 'Megaminx',
	pyram: 'Pyraminx',
	clock: 'Clock',
	skewb: 'Skewb',
	sq1: 'Square-1',
	'444bf': '4x4x4 Blindfolded',
	'555bf': '5x5x5 Blindfolded',
	'333mbf': '3x3x3 Multi-Blind'
} as const;

export interface Person {
	name: string;
	times: string[];
}

export interface EventResults {
	name: string;
	rounds: {
		[roundNumber: string]: Person[];
	};
}

export interface CompetitionResults {
	competition: Competition;
	results: {
		[event in WCAEvent]?: EventResults;
	};
}
