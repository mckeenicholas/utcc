import { eventSolves, type Person, type WCAEvent } from './types';

const isProduction = process.env.NODE_ENV === 'production';
const BASE_URL = isProduction ? 'https://utcc.nmckee.org' : 'http://localhost';

export const resultsURL = `${BASE_URL}/api/results/`;
export const competitionsURL = `${BASE_URL}/api/results/competitions/`;
export const recordsURL = `${BASE_URL}/api/results/records/`;

const compareTime = (time1: number, time2: number) => {
	if (time1 > 0 && time2 > 0) return time1 - time2;
	if (time1 < 0 && time2 > 0) return 1;
	if (time1 > 0 && time2 < 0) return -1;
	if (time1 == 0 && time2 != 0) return 1;
	if (time1 != 0 && time2 == 0) return -1;

	return 0;
};

export const compareResults = (person1: Person, person2: Person): number => {
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
