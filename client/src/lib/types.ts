import type { scrambleOrder } from "./utils";

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
	session: number | null;
	session_name: string | null;
	student_designator: string;
	has_results?: boolean;
}

export const studentDesignatorOptions = [
	{ label: "UTSG", value: "UTSG" },
	{ label: "UTM", value: "UTM" },
	{ label: "UTSC", value: "UTSC" },
	{ label: "Non-UofT", value: "Non-UofT" },
];

export type WCAEvent = keyof typeof eventNames;

export const eventNames = {
	"222": "2x2x2 Cube",
	"333": "3x3x3 Cube",
	"333bf": "3x3x3 Blindfolded",
	"333fm": "3x3x3 Fewest Moves",
	"333mbf": "3x3x3 Multi-Blind",
	"333oh": "3x3x3 One-Handed",
	"444": "4x4x4 Cube",
	"444bf": "4x4x4 Blindfolded",
	"555": "5x5x5 Cube",
	"555bf": "5x5x5 Blindfolded",
	"666": "6x6x6 Cube",
	"777": "7x7x7 Cube",
	clock: "Clock",
	minx: "Megaminx",
	pyram: "Pyraminx",
	skewb: "Skewb",
	sq1: "Square-1",
} as const;

export const isWCAEvent = (key: string): key is WCAEvent => key in eventNames;

export const WCAEventList = Object.keys(eventNames).filter((key) => isWCAEvent(key));

export const eventSolves: Partial<Record<WCAEvent, number>> = {
	"222": 5,
	"333": 5,
	"333bf": 3,
	"333fm": 3,
	"333oh": 5,
	"444": 5,
	"444bf": 3,
	"555": 5,
	"555bf": 3,
	"666": 3,
	"777": 3,
	clock: 5,
	minx: 5,
	pyram: 5,
	skewb: 5,
	sq1: 5,
} as const;

export const eventListIdx: Record<WCAEvent, number> = {
	"222": 1,
	"333": 0,
	"333bf": 6,
	"333fm": 7,
	"333mbf": 16,
	"333oh": 8,
	"444": 2,
	"444bf": 14,
	"555": 3,
	"555bf": 15,
	"666": 4,
	"777": 5,
	clock: 9,
	minx: 10,
	pyram: 11,
	skewb: 12,
	sq1: 13,
} as const;

export interface BaseResult {
	id: number;
	single: number;
	average: number;
	person_name: string;
	person: number;
}

export interface PersonResult extends BaseResult {
	times: number[];
}

export interface PersonResultStudentStatus extends PersonResult {
	student_designator: string;
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
	results: PersonResultStudentStatus[];
	scramble_sets: ResultScrambleSet[];
}

export interface ResultScrambleSet {
	scramble_set: number;
	scrambles: Scramble[];
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
	person: number;
	competition_name: string;
	competition_id: number;
	rank: number;
}

export interface EventRecords {
	single?: RecordInstance;
	average?: RecordInstance;
}

export type RecordsApiResponse = Partial<Record<WCAEvent, EventRecords>>;

export interface User {
	id: number;
	name: string;
	student_designator: string;
	sessions: Session[];
}

export interface ProfileRecordDetail {
	single: number;
	average: number | null;
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

export interface Session {
	id: number;
	name: string;
	start_date: string;
}

export type ResultsTableCompetition = Omit<ProfileEventCompetition, "date">;

export interface UserProfileResponse {
	name: string;
	records: [WCAEvent, ProfileRecordDetail][];
	results: { event: WCAEvent; results: ResultsTableCompetition[] }[];
}

export type StudentStatus = string[];

export interface Scramble {
	id: number;
	scramble_num: number;
	scramble: string;
}

export type CompetitionScrambleSets = {
	event: WCAEvent;
	rounds: {
		round: number;
		sets: { id: number; scramble_set: number; visible: boolean }[];
	}[];
}[];

export interface ScrambleResponse {
	competition: string;
	event: WCAEvent;
	round: number;
	scrambles: Scramble[];
}

export type ScrambleKey = keyof typeof scrambleOrder;
