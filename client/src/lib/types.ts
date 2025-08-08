export interface Paginated<T> {
	count: number;
	next: string | null;
	previous: string | null;
	results: T[];
}

export interface Competition {
	id: number;
	name: string;
	date: string;
	events: WCAEvent[];
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

export const WCAEventList = Object.keys(eventNames) as WCAEvent[];

export const eventSolves: Partial<Record<WCAEvent, number>> = {
	'333': 5,
	'222': 5,
	'444': 5,
	'555': 5,
	'666': 3,
	'777': 3,
	'333bf': 3,
	'333fm': 3,
	'333oh': 5,
	minx: 5,
	pyram: 5,
	clock: 5,
	skewb: 5,
	sq1: 5,
	'444bf': 3,
	'555bf': 3
} as const;

export const eventListIdx: Record<WCAEvent, number> = {
	'333': 0,
	'222': 1,
	'444': 2,
	'555': 3,
	'666': 4,
	'777': 5,
	'333bf': 6,
	'333fm': 7,
	'333oh': 8,
	clock: 9,
	minx: 10,
	pyram: 11,
	skewb: 12,
	sq1: 13,
	'444bf': 14,
	'555bf': 15,
	'333mbf': 16
} as const;

export interface BaseResult {
	id: number;
	single: number;
	average: number;
	person_name: string;
	person_id: number;
}

export interface PersonResult extends BaseResult {
	times: number[];
}

export interface Result extends BaseResult {
	competition: number;
	event: WCAEvent;
	round: number;
	time1: number;
	time2: number;
	time3: number;
	time4: number;
	time5: number;
}

export interface Round {
	round: number;
	results: PersonResult[];
}

export interface EventResult {
	event: WCAEvent;
	rounds: Round[];
}

export interface CompetitionResults {
	competition: Competition;
	results: EventResult[];
}

export interface RecordInstance {
	result: number;
	times_list: number[];
	person_name: string;
	person_id: number;
	competition_name: string;
	competition_id: number;
}

export interface EventRecords {
	single?: RecordInstance;
	average?: RecordInstance;
}

export interface RecordsApiResponse {
	WCAEvent?: EventRecords;
}

export interface User {
	id: number;
	name: string;
}

export interface ProfileRecordDetail {
	single: number;
	average: number;
}

export interface ProfileRoundResult {
	round: number;
	times: number[];
	single: number;
	average: number;
	singleRecord?: boolean;
	averageRecord?: boolean;
}

export interface ProfileEventCompetition {
	id: number;
	name: string;
	date: string;
	rounds: ProfileRoundResult[];
}

export interface ProfileEventResult {
	event: WCAEvent;
	competitions: ProfileEventCompetition[];
}

export type PersonalRecords = Partial<Record<WCAEvent, ProfileRecordDetail>>;

export interface ProfileResponse {
	person: User;
	records: PersonalRecords;
	results: ProfileEventResult[];
}
