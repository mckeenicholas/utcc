import { dev } from '$app/environment';
import {
	eventListIdx,
	eventSolves,
	type PersonalRecords,
	type PersonResult,
	type ProfileEventResult,
	type ProfileRoundResult,
	type WCAEvent
} from './types';

export const BASE_URL = dev ? 'http://localhost:8000' : 'https://utcc.nmckee.org';

// Updated URLs to match backend structure
export const latestCompetitionsURL = `${BASE_URL}/api/competitions/`;
export const latestResultsURL = `${BASE_URL}/api/competitions/latest/results/`;
export const recordsURL = `${BASE_URL}/api/records/`;

export const PAGINATION_SIZE = 20;

const compareTime = (time1: number, time2: number) => {
	if (time1 > 0 && time2 > 0) return time1 - time2;
	if (time1 < 0 && time2 > 0) return 1;
	if (time1 > 0 && time2 < 0) return -1;
	if (time1 == 0 && time2 != 0) return 1;
	if (time1 != 0 && time2 == 0) return -1;

	return 0;
};

export const compareResults = (person1: PersonResult, person2: PersonResult): number => {
	const averageComparison = compareTime(person1.average, person2.average);
	if (averageComparison != 0) return averageComparison;

	return compareTime(person1.single, person2.single);
};

export const renderTime = (time: number | null): string => {
	if (!time) {
		return '';
	}

	if (time == -2) {
		return 'DNS';
	}

	if (time == -1) {
		return 'DNF';
	}

	const seconds = time / 100;

	if (seconds >= 60) {
		const minutes = Math.floor(seconds / 60);
		const remainingSeconds = (seconds % 60).toFixed(2);
		// Pad seconds with leading zero if needed
		return `${minutes}:${remainingSeconds.padStart(5, '0')}`;
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
				averageRecord: false
			}))
		}))
		.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

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
			null as ProfileRoundResult | null
		);

		const bestAverageRound = competition.rounds.reduce(
			(best, current) => {
				if (current.average > 0 && current.average < (best?.average || Infinity)) {
					return current;
				}
				return best;
			},
			null as ProfileRoundResult | null
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

	return { event: results.event, results: processedResults.reverse() };
};

export const getMeanType = (event: WCAEvent) => {
	if (eventSolves[event] == 3) return 'Mean';

	return 'Average';
};

export const checkLoginStatus = async () => {
	const loggedInData = await fetchJson<{ logged_in: boolean }>(
		`${BASE_URL}/api/users/auth/status/`,
		{ credentials: 'include' }
	);
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
