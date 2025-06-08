import { eventSolves, type WCAEvent } from './types';

const isProduction = process.env.NODE_ENV === 'production';
const BASE_URL = isProduction ? 'https://utcc.nmckee.org' : 'http://localhost';

export const resultsURL = `${BASE_URL}/api/results/`;
export const competitionsURL = `${BASE_URL}/api/results/competitions/`;

export const Ao5 = (times: number[]): number => {
	if (times.length !== 5) {
		throw new Error('Ao5 requires exactly 5 times');
	}

	const dnfCount = times.filter((t) => t === -1).length;
	if (dnfCount >= 2) {
		return -1;
	}

	const validTimes = times.map((t) => (t === -1 ? Infinity : t));
	const sortedTimes = [...validTimes].sort((a, b) => a - b);
	const middleThree = sortedTimes.slice(1, 4);

	if (middleThree.includes(Infinity)) {
		return -1;
	}

	return Math.trunc(middleThree.reduce((sum, t) => sum + t, 0) / 3);
};

export const Mo3 = (times: number[]): number => {
	if (times.length !== 3) {
		throw new Error('Mo3 requires exactly 3 times');
	}

	if (times.includes(-1)) {
		return -1;
	}

	return Math.trunc(times.reduce((sum, t) => sum + t, 0) / 3);
};

export const Bo3 = (times: number[]): number => {
	if (times.length !== 3) {
		throw new Error('Bo3 requires exactly 3 times');
	}

	return Math.min(...times);
};

export const calculateWCAAverage = (event: WCAEvent, times: number[]): number => {
	const validTimes = times.filter((t) => t != 0).length;

	if (validTimes < 3) {
		return 0;
	}

	if (event === '666' || event === '777' || event === '333fm') {
		return Mo3(times);
	}

	if (event === '333bf' || event === '444bf' || event === '555bf') {
		return Bo3(times);
	}

	if (validTimes < 5) {
		return 0;
	}
	return Ao5(times);
};

export const compareTimes = (event: WCAEvent, times1: number[], times2: number[]): number => {
	const required = eventSolves[event] || 5;
	const validTimes1 = times1.filter((t) => t != 0).length;
	const validTimes2 = times2.filter((t) => t != 0).length;

	// If one set is complete and the other isn't, the complete set ranks better
	if (validTimes1 >= required && validTimes2 < required) return -1;
	if (validTimes2 >= required && validTimes1 < required) return 1;

	// If both sets are complete, compare by average
	if (validTimes1 >= required && validTimes2 >= required) {
		const res = calculateWCAAverage(event, times1) - calculateWCAAverage(event, times2);
		if (res !== 0) {
			return res;
		}
	}

	// If both sets are incomplete or tied on average, compare best times
	return Math.min(...times1.filter((t) => t > 0)) - Math.min(...times2.filter((t) => t > 0));
};

export const bestTime = (times: number[]): number => {
	const validTimes = times.filter((time) => time > 0);

	if (validTimes.length == 0) {
		return -1;
	}

	return Math.min(...validTimes);
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
