import * as firebase from "firebase";

import { firebaseConfig } from "../config/keys";
firebase.initializeApp(firebaseConfig);

const databaseRef = firebase.database().ref();
export const attendenceRef = databaseRef.child("attendence");
export const SuspiciousRef = databaseRef.child("Suspicious");
export const UnauthorizedRef = databaseRef.child("Unauthorized");
export const authRef = firebase.auth();
export const provider = new firebase.auth.GoogleAuthProvider();