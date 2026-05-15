import { dev } from "$app/environment";
import {
	eventListIdx,
	eventSolves,
	type PersonalRecords,
	type PersonResult,
	type ProfileEventResult,
	type ProfileRoundResult,
	type WCAEvent,
} from "./types";

export const BASE_URL = dev ? "http://localhost:8000" : "https://utcc.nmckee.org";

// Updated URLs to match backend structure
export const latestCompetitionsURL = `${BASE_URL}/api/competitions/`;
export const latestResultsURL = `${BASE_URL}/api/competitions/latest/results/`;
export const recordsURL = `${BASE_URL}/api/records/`;

export const PAGINATION_SIZE = 20;

const compareTime = (time1: number, time2: number) => {
	if (time1 > 0 && time2 > 0) {
		return time1 - time2;
	}
	if (time1 < 0 && time2 > 0) {
		return 1;
	}
	if (time1 > 0 && time2 < 0) {
		return -1;
	}
	if (time1 == 0 && time2 != 0) {
		return 1;
	}
	if (time1 != 0 && time2 == 0) {
		return -1;
	}

	return 0;
};

export const compareResults = (person1: PersonResult, person2: PersonResult): number => {
	const averageComparison = compareTime(person1.average, person2.average);
	if (averageComparison != 0) {
		return averageComparison;
	}

	return compareTime(person1.single, person2.single);
};

export const renderTime = (time: number | null): string => {
	if (!time) {
		return "";
	}

	if (time == -2) {
		return "DNS";
	}

	if (time == -1) {
		return "DNF";
	}

	const seconds = time / 100;

	if (seconds >= 60) {
		const minutes = Math.floor(seconds / 60);
		const remainingSeconds = (seconds % 60).toFixed(2);
		// Pad seconds with leading zero if needed
		return `${minutes}:${remainingSeconds.padStart(5, "0")}`;
	}

	return seconds.toFixed(2);
};

// Formats data in correct order for person records table.
export const processPersonalRecords = (records: PersonalRecords) => {
	const recordEntries = Object.entries(records);
	recordEntries.sort((a, b) => {
		const eventA = a[0] as WCAEvent;
		const eventB = b[0] as WCAEvent;
		return eventListIdx[eventA] - eventListIdx[eventB];
	});
	return recordEntries;
};

// Calculates PRs to highlight and formats data for the results table
export const generateRecordsForEvent = (results: ProfileEventResult) => {
	const processedResults = results.competitions
		.map((comp) => ({
			...comp,
			rounds: comp.rounds.map((round) => ({
				...round,
				singleRecord: false,
				averageRecord: false,
			})),
		}))
		.toSorted((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

	let singleRecordTime = Infinity;
	let averageRecordTime = Infinity;

	for (const competition of processedResults) {
		const bestSingleRound = competition.rounds.reduce(
			(best, current) => {
				if (current.single > 0 && current.single < (best?.single || Infinity)) {
					return current;
				}
				return best;
			},
			null as ProfileRoundResult | null,
		);

		const bestAverageRound = competition.rounds.reduce(
			(best, current) => {
				if (current.average > 0 && current.average < (best?.average || Infinity)) {
					return current;
				}
				return best;
			},
			null as ProfileRoundResult | null,
		);

		if (bestSingleRound && bestSingleRound.single < singleRecordTime) {
			singleRecordTime = bestSingleRound.single;
			bestSingleRound.singleRecord = true;
		}

		if (bestAverageRound && bestAverageRound.average < averageRecordTime) {
			averageRecordTime = bestAverageRound.average;
			bestAverageRound.averageRecord = true;
		}
	}

	return { event: results.event, results: processedResults.toReversed() };
};

export const getMeanType = (event: WCAEvent) => {
	if (eventSolves[event] == 3) {
		return "Mean";
	}

	return "Average";
};

export const checkLoginStatus = async () => {
	const loggedInData = await fetchJson<{ logged_in: boolean }>(`${BASE_URL}/api/users/auth/status/`, {
		credentials: "include",
	});
	return loggedInData.logged_in;
};

export const formatCompetitionDate = (dateStr: string) => {
	const utcDate = new Date(`${dateStr}T12:00:00Z`);
	return utcDate.toLocaleDateString();
};

export const fetchJson = async <T>(url: string | URL, options?: RequestInit): Promise<T> => {
	const response = await fetch(url, options);

	if (!response.ok) {
		throw new Error(`Failed to fetch: ${response.statusText}`);
	}

	const data: T = await response.json();
	return data;
};

export const sortEvents = (a: WCAEvent, b: WCAEvent) => {
	return eventListIdx[a] - eventListIdx[b];
};

export const scrambleOrder = {
	"-2": { idx: 7, name: "E2" },
	"-1": { idx: 6, name: "E1" },
	"1": { idx: 1, name: "1" },
	"2": { idx: 2, name: "2" },
	"3": { idx: 3, name: "3" },
	"4": { idx: 4, name: "4" },
	"5": { idx: 5, name: "5" },
} as const;

export const formatScramble = (scrambleStr: string, event: WCAEvent) => {
	const cubeMovesPerLine = 12;
	const sq1ClockMovesPerLine = 5;
	const cubeMaxMoveLength = 4; // Maximum length of a move (e.g., "3Rw'")
	const sq1ClockMaxMoveLength = 8;

	if (event == "minx") {
		const lines = scrambleStr.split("\n").map((line) => line + " ");
		return { lines, numLines: lines.length };
	}

	const splitChar = event == "sq1" ? " / " : " ";
	const moves = scrambleStr.split(splitChar);
	const lines = [];

	const movesPerLine = event == "sq1" || event == "clock" ? sq1ClockMovesPerLine : cubeMovesPerLine;
	const maxMoveLength = event == "sq1" || event == "clock" ? sq1ClockMaxMoveLength : cubeMaxMoveLength;

	for (let i = 0; i < moves.length; i += movesPerLine) {
		const lineMoves = moves.slice(i, i + movesPerLine);
		const paddedMoves = lineMoves.map((move) => {
			if (event === "sq1") {
				// Split the tuple (e.g., "(1, -5)") into its numbers
				const [top, bottom] = move
					.slice(1, -1)
					.split(",")
					.map((s) => s.trim());

				// Add a space before positive numbers for alignment
				const paddedTop = top.startsWith("-") ? top : ` ${top}`;
				const paddedBottom = bottom.startsWith("-") ? bottom : ` ${bottom}`;

				return `(${paddedTop},${paddedBottom})`;
			}
			return move.padEnd(maxMoveLength);
		});
		lines.push(paddedMoves.join(splitChar));
	}

	return { lines: lines, numLines: lines.length };
};
