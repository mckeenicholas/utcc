import { eventSolves, type PersonResult, type WCAEvent } from './types';

const isProduction = process.env.NODE_ENV === 'production';
export const BASE_URL = isProduction ? 'https://utcc.nmckee.org' : 'http://localhost:8000';

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

export const renderTime = (time: number): string => {
	if (time == -2) {
		return 'DNS';
	}

	if (time == -1) {
		return 'DNF';
	}

	if (time == 0) {
		return '';
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

export const getMeanType = (event: WCAEvent) => {
	if (eventSolves[event] == 3) return 'Mean';

	return 'Average';
};

export const checkLoginStatus = async () => {
	const loggedInRes = await fetch(`${BASE_URL}/api/users/auth/status/`, { credentials: 'include' });
	const loggedInData = await loggedInRes.json();

	return loggedInData.logged_in;
};
