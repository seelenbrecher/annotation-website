<template>
<section class="ftco-section">
    <div ref="administrator" class="container">
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-10">
                <div class="wrap d-md-flex p-3">
                    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                        <li class="nav-item mr-auto" role="presentation">
                            <button class="nav-link active position-relative" id="annotating-label" type="button">Annotating Database: {{ annotating_database }}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ count }} claim
                                </span>
                            </button>
                            <h6 class="mt-0 pt-2 pl-3 pb-2 annotator"> Annotator: {{ annotator_email }}</h6>
                        </li>
                    </ul>
                    <button @click="homepage" type="submit" class="form-control btn btn-dark submit px-3 home-button ml-auto">
                        <span class="badge text-bg-light ml-3 annotate-next">
                            Back to Home
                        </span>
                    </button>
                </div>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-10">
                <div class="wrap d-md-flex">
                    <template v-if="annotationTodo && count != 0">
                        <div class="login-wrap p-4 p-lg-5 w-100">
                            <div class="d-flex">
                                <div class="w-100">
                                    <span class="badge text-bg-primary claim-badge">Claim</span>
                                    <h3 class="mb-4 claim-text" ref="temporalListner">{{ annotationTodo.content }}</h3>
                                </div>
                            </div>
                            <p>Be default, all claims uploaded should be temporal. Select non-temporal if the claim does not contain any time information and annotation is not required on the claim.</p>
                            <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
                                <input type="radio" v-model="overallTemporalFlag" class="btn-check" name="obtnradio" id="obtnradio1" value="true" autocomplete="off" checked>
                                <label class="btn btn-outline-primary" for="obtnradio1">Temporal</label>

                                <input type="radio" v-model="overallTemporalFlag" class="btn-check" name="obtnradio" id="obtnradio2" value="false" autocomplete="off">
                                <label class="btn btn-outline-primary" for="obtnradio2">Non-temporal</label>
                            </div>
                            <template v-if="overallTemporalFlag == 'true'">
                                <template v-for="item in annotationTodo.evidences" :key="item.id">
                                    <div class="form-group mb-3 evidence-div p-2">
                                        <span class="badge text-bg-primary claim-badge">Evidence</span>
                                        <label class="label ml-3" for="title">{{ item.title }}</label>
                                        <div class="d-flex">
                                            <div class="w-100">
                                                <h5 class="mb-2 evidence-text" :id=item.id>{{ item.content }}</h5>
                                            </div>
                                        </div>
                                    </div>
                                </template>
                                <div class="row mb-4 mt-4">
                                    <div class="col-md-12 col-lg-12 annotation text-left">
                                        <template v-if="section == 0">
                                            <div class="form-group mb-1">
                                                <span class="badge text-bg-primary label-badge">Label</span>
                                            </div>
                                            <div class="btn-group w-100" role="group" aria-label="Basic radio toggle button group">
                                                <input type="radio" v-model="temporalFlag" @click="selectTemporal" class="btn-check label-button" name="gbtnradio" id="temporalbtnradio1" value=0 autocomplete="off">
                                                <label class="btn btn-outline-primary label-button" for="temporalbtnradio1">Supports</label>

                                                <input type="radio" v-model="temporalFlag" @click="selectTemporal" class="btn-check label-button" name="gbtnradio" id="temporalbtnradio2" value=1 autocomplete="off">
                                                <label class="btn btn-outline-primary label-button" for="temporalbtnradio2">Refutes</label>

                                                <input type="radio" v-model="temporalFlag" @click="selectTemporal" class="btn-check label-button" name="gbtnradio" id="temporalbtnradio3" value=2 autocomplete="off">
                                                <label class="btn btn-outline-primary label-button" for="temporalbtnradio3">Not Enough Information</label>
                                            </div>
                                            <p v-if="temporalFlag == null" class="text-center"> Please select a label.</p>
                                            <div class="form-group text-right">
                                                <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button mt-2" :disabled="temporalFlag == null">
                                                    <span class="badge text-bg-light ml-3 annotate-next">
                                                        Next claim
                                                    </span>
                                                </button>
                                            </div>
                                        </template>
                                        <template v-if="section == 1">
                                            <span class="badge text-bg-primary label-badge">Justification for Temporal Label</span>
                                            <p v-if="temporalFlag == 0">You have selected "Supports" for the temporal classification. Please use your mouse to select which temporal part of the evidence texts support the temporal parts of the claim.</p>
                                            <p v-if="temporalFlag == 1">You have selected "Refutes" for the temporal classification. Please use your mouse to select which temporal part of the evidence texts refutes the temporal parts of the claim.</p>
                                            <p v-if="temporalFlag == 2">You have selected "Not Enough Information" for the temporal classification. Please use your mouse to select which temporal part of the claim text was not able to be successfully annotated with the given evidences.</p>
                                            <ul v-if="temporalFlag != null" class="list-group list-group-horizontal temporal_justification mb-3 p-1">
                                                <template v-for="(item, index) in temporalJustification" :key="item">
                                                    <li class="list-group-item temporal-item">
                                                        {{ item }}
                                                        <a href v-on:click.prevent="deleteTemporalJustification" :id="index"> <span class="badge bg-danger rounded-pill">
                                                                <font-awesome-icon icon="fa-solid fa-times" /></span></a>
                                                    </li>
                                                </template>
                                            </ul>
                                            <div class="form-group text-center">
                                                <button @click="previousAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2 mr-3">
                                                    <span class="badge text-bg-light ml-3 annotate-next">
                                                        Back to temporal label
                                                    </span>
                                                </button>
                                                <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2" :disabled="temporalFlag == null || temporalJustification.length == 0">
                                                    <span class="badge text-bg-light ml-3 annotate-next">
                                                        Next to general label
                                                    </span>
                                                </button>
                                            </div>
                                        </template>
                                        <template v-if="section == 2">
                                            <div class="form-group mb-1">
                                                <span class="badge text-bg-primary label-badge">General Facts Label</span>
                                            </div>
                                            <div class="btn-group w-100" role="group" aria-label="Basic radio toggle button group">
                                                <input type="radio" v-model="generalFlag" @click="selectGeneral" class="btn-check label-button" name="tbtnradio" id="generalbtnradio1" value=0 autocomplete="off">
                                                <label class="btn btn-outline-primary label-button" for="generalbtnradio1">Supports</label>

                                                <input type="radio" v-model="generalFlag" @click="selectGeneral" class="btn-check label-button" name="tbtnradio" id="generalbtnradio2" value=1 autocomplete="off">
                                                <label class="btn btn-outline-primary label-button" for="generalbtnradio2">Refutes</label>

                                                <input type="radio" v-model="generalFlag" @click="selectGeneral" class="btn-check label-button" name="tbtnradio" id="generalbtnradio3" value=2 autocomplete="off">
                                                <label class="btn btn-outline-primary label-button" for="generalbtnradio3">Not Enough Information</label>
                                            </div>
                                            <div class="form-group text-center">
                                                <button @click="previousAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-3 mt-2 mr-3">
                                                    <span class="badge text-bg-light ml-3 annotate-next">
                                                        Back to temporal justification
                                                    </span>
                                                </button>
                                                <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-3 mt-2" :disabled="generalFlag == null">
                                                    <span class="badge text-bg-light ml-3 annotate-next">
                                                        Next to general justification
                                                    </span>
                                                </button>
                                            </div>
                                        </template>
                                        <template v-if="section == 3">
                                            <span class="badge text-bg-primary label-badge">Justification for General Label</span>
                                            <p v-if="generalFlag == 0">You have selected "Supports" for the general classification. Please use your mouse to select which general part of the evidence texts support the general parts of the claim.</p>
                                            <p v-if="generalFlag == 1">You have selected "Refutes" for the general classification. Please use your mouse to select which general part of the evidence texts refutes the general parts of the claim.</p>
                                            <p v-if="generalFlag == 2">You have selected "Not Enough Information" for the general classification. Please use your mouse to select which general part of the claim text was not able to be successfully annotated with the given evidences.</p>
                                            <ul v-if="generalFlag != null" class="list-group list-group-horizontal temporal_justification mb-3 p-1">
                                                <template v-for="(item, index) in generalJustification" :key="item">
                                                    <li class="list-group-item temporal-item">
                                                        {{ item }}
                                                        <a href v-on:click.prevent="deleteGeneralJustification" :id="index"> <span class="badge bg-danger rounded-pill">
                                                                <font-awesome-icon icon="fa-solid fa-times" /></span></a>
                                                    </li>
                                                </template>
                                            </ul>
                                            <div class="form-group text-center">
                                                <button @click="previousAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2 mr-3">
                                                    <span class="badge text-bg-light ml-3 annotate-next">
                                                        Back to general label
                                                    </span>
                                                </button>
                                                <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2" :disabled="generalFlag == null || generalJustification.length == 0">
                                                    <span class="badge text-bg-light ml-3 annotate-next">
                                                        Finish Annotation
                                                    </span>
                                                    <span v-if="count != 1" class="badge text-bg-light ml-3 move-on">
                                                        and move on to the next one
                                                    </span>
                                                    <span v-else class="badge text-bg-light ml-3 move-on">
                                                        no more claims to annotate
                                                    </span>
                                                </button>
                                            </div>
                                        </template>
                                    </div>
                                </div>
                            </template>
                            <template v-else>
                                <div class="form-group text-right">
                                    <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2">
                                        <span class="badge text-bg-light ml-3 annotate-next">
                                            Finish Annotation
                                        </span>
                                        <span v-if="count != 1" class="badge text-bg-light ml-3 move-on">
                                            and move on to the next one
                                        </span>
                                        <span v-else class="badge text-bg-light ml-3 move-on">
                                            no more claims to annotate
                                        </span>
                                    </button>
                                </div>
                            </template>
                            <div class="form-group d-md-flex">
                                <div class="w-100 text-md-right">
                                    <a href v-on:click.prevent="login = !login">Report a problem
                                        <font-awesome-icon icon="fa-solid fa-circle-arrow-right" /> </a>
                                </div>
                            </div>
                        </div>
                    </template>
                    <div v-if="count == 0" class="login-wrap p-4 p-lg-5 w-100">
                        <h2 class="">Sorry, there are no annotation claims left to do.</h2>
                    </div>
                    <div v-if="count == null" class="login-wrap p-4 p-lg-5 w-100">
                        <div class="spinner-border m-5" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <h2>Processing</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
import { useToast } from "vue-toastification";
export default {
    setup() {
        // Get toast interface
        const toast = useToast();
        // Set up Pinia User store
        const store = useUserStore();
        const controller1 = new AbortController();
        const controller2 = new AbortController();
        return { store, toast, controller1, controller2 }
    },
    name: 'Home',
    data() {
        return {
            annotationTodo: "",
            count: null,

            overallTemporalFlag: 'true',
            temporalFlag: null,
            generalFlag: null,

            temporalJustification: [],
            temporalJustificationEvidenceIds: [],
            generalJustification: [],
            generalJustificationEvidenceIds: [],

            // Indicates which step annotator is on, 0 - select temporal label, 1 - justify temporal label, 2 - select general label, 3 - justify general label
            section: 0,

        }
    },
    computed: {
        annotating_database() {
            return this.store.annotatingDatabase
        },
        annotator_email() {
            return this.store.annotatorEmail
        },
    },
    mounted() {
        // Check if key store values are set, otherwise redirect
        if (this.store.annotatorEmail == "" || this.store.annotatingDatabase == "" || this.store.isAuthenticatedAnnotation == false) {
            this.$router.push({ name: 'unauthorised' })
        }
    },
    created() {
        // Axios call to fetch first entry for annotation 
        const annotateData = {
            annotatorEmail: this.store.annotatorEmail,
            databaseId: this.store.annotatingDatabase,
        }
        axios
            .post('/api/v1/database/annotation/get/', annotateData)
            .then(response => {
                console.log(response.data)
                this.annotationTodo = response.data.firstItem
                this.count = response.data.count
            })
            .catch(error => {
                // Request was made and server responded unfavourably
                if (error.response.data.non_field_errors[0]) {
                    this.toast.error(error.response.data.non_field_errors[0]);
                }
                // Request was made but no response received
                else if (error.request) {
                    this.toast.error("Received no response from the server. Please try again.");
                }
                // Something else happened
                else {
                    this.toast.error("Sorry, an unknown error occurred. Please try again.");
                }
            })
    },
    methods: {
        homepage() {
            this.$router.push({ name: 'homepage' })
        },
        nextAnnotationProcess() {
            if (this.overallTemporalFlag == 'true') {
                // this.section = this.section + 1;
                // if (this.section == 1 || this.section == 3) {
                //     this.captureJustifications();
                // }
                // if (this.section == 4) {
                //     this.nextAnnotate()
                // }
                this.nextAnnotate()
            } else {
                this.nextAnnotate()
            }
        },
        previousAnnotationProcess() {
            this.section = this.section - 1;
            if (this.section == 1 || this.section == 3) {
                this.captureJustifications();
            }
        },
        selectTemporal() {
            this.temporalJustification = [];
            this.temporalJustificationEvidenceIds = [];
        },
        selectGeneral() {
            this.generalJustification = [];
            this.generalJustificationEvidenceIds = [];
        },
        captureJustifications() {
            if (this.section == 1) {
                // Temporal justifications
                if (this.temporalFlag == 2) {
                    this.captureTemporalJustificationsNotEnoughInformation();
                } else {
                    this.captureTemporalJustificationsSupportsRefutes();
                }
            } else {
                // General justifications
                if (this.generalFlag == 2) {
                    this.captureGeneralJustificationsNotEnoughInformation();
                } else {
                    this.captureGeneralJustificationsSupportsRefutes();
                }
            }
        },
        captureTemporalJustificationsNotEnoughInformation() {
            document.removeEventListener('mouseup', this.eventListenerEvidence)
            document.removeEventListener('mouseup', this.generalEventListenerEvidence)
            this.$refs.temporalListner.removeEventListener('mouseup', this.generalEventListener)
            this.$refs.temporalListner.addEventListener('mouseup', this.eventListener)
        },
        captureTemporalJustificationsSupportsRefutes() {
            this.$refs.temporalListner.removeEventListener('mouseup', this.eventListener)
            this.$refs.temporalListner.removeEventListener('mouseup', this.generalEventListener)
            document.removeEventListener('mouseup', this.generalEventListenerEvidence)
            document.addEventListener('mouseup', this.eventListenerEvidence)
        },
        captureGeneralJustificationsNotEnoughInformation() {
            document.removeEventListener('mouseup', this.generalEventListenerEvidence)
            document.removeEventListener('mouseup', this.eventListenerEvidence)
            this.$refs.temporalListner.removeEventListener('mouseup', this.eventListener)
            this.$refs.temporalListner.addEventListener('mouseup', this.generalEventListener)
        },
        captureGeneralJustificationsSupportsRefutes() {
            this.$refs.temporalListner.removeEventListener('mouseup', this.generalEventListener)
            this.$refs.temporalListner.removeEventListener('mouseup', this.eventListener)
            document.removeEventListener('mouseup', this.eventListenerEvidence)
            document.addEventListener('mouseup', this.generalEventListenerEvidence)
        },
        addTemporalJustification(e) {
            if (window.getSelection().toString().trim() != "") {
                // Prevent duplicate justification text from being added
                if (!this.temporalJustification.includes(window.getSelection().toString().trim())) {
                    this.temporalJustification.push(window.getSelection().toString().trim())
                    // Do not want to add evidence ids if it is adding claim details
                    if (this.temporalFlag != 2) {
                        this.temporalJustificationEvidenceIds.push(parseInt(e.target.id))
                    }
                }
            }
        },
        addGeneralJustification(e) {
            if (window.getSelection().toString().trim() != "") {
                if (!this.generalJustification.includes(window.getSelection().toString().trim())) {
                    // Prevent duplicate justification text from being added
                    this.generalJustification.push(window.getSelection().toString().trim())
                    if (this.generalFlag != 2) {
                        this.generalJustificationEvidenceIds.push(parseInt(e.target.id))
                    }
                }
            }
        },
        generalEventListener: function (event) {
            this.addGeneralJustification(event);
        },
        generalEventListenerEvidence: function (event) {
            if (event.target.classList.contains('evidence-text')) {
                this.addGeneralJustification(event);
            }
        },
        eventListener: function (event) {
            this.addTemporalJustification(event);
        },
        eventListenerEvidence: function (event) {
            if (event.target.classList.contains('evidence-text')) {
                this.addTemporalJustification(event);
            }
        },
        deleteTemporalJustification: function (e) {
            const id = e.currentTarget.id;
            this.temporalJustification.splice(id, 1);
            // Do not delete from ids if it was a claim removal
            if (this.temporalFlag != 2) {
                this.temporalJustificationEvidenceIds.splice(id, 1);
            }
        },
        deleteGeneralJustification: function (e) {
            const id = e.currentTarget.id;
            this.generalJustification.splice(id, 1);
            // Do not delete from ids if it was as claim removal
            if (this.generalFlag != 2) {
                this.generalJustificationEvidenceIds.splice(id, 1);
            }
        },
        processFlags(flag) {
            if (flag == 0) {
                return "SUPPORTS"
            } else if (flag == 1) {
                return "REFUTES"
            } else {
                return "NOT ENOUGH INFORMATION"
            }
        },
        processOverallFlag(temporal, general) {
            // Flags can only be 0, 1 or 2
            // If either one refutes, return refute
            if (temporal == 1 || general == 1) {
                return "REFUTES"
                // If either one is not enough info, return not enough info
            } else if (temporal == 2 || general == 2) {
                return "NOT ENOUGH INFORMATION"
            } else {
                return "SUPPORTS"
            }
        },
        submitAnnotation() {
            // Submit annotation then add justification in
            var submittedAnnotateData;
            if (this.overallTemporalFlag == 'true') {
                submittedAnnotateData = {
                    claimId: this.annotationTodo.id,
                    email: this.store.annotatorEmail,
                    overall_temporal_claim: true,
                    temporal_flag: this.processFlags(this.temporalFlag),
                    general_flag: this.processFlags(0),
                    overall_flag: this.processOverallFlag(this.temporalFlag)
                }
            } else {
                submittedAnnotateData = {
                    claimId: this.annotationTodo.id,
                    email: this.store.annotatorEmail,
                    overall_temporal_claim: false,
                }
            }
            axios
                .post('/api/v1/database/annotation/add/', submittedAnnotateData)
                .then(initialresponse => {
                    console.log(initialresponse.data)
                    if (this.overallTemporalFlag == 'true') {
                        // Add justification after annotation successfully added
                        for (var i = 0; i < this.temporalJustification.length; i++) {
                            const justificationText = this.temporalJustification[i]
                            var submittedJustificationData;
                            // For claim justificaion, no need add evidence ids
                            if (this.temporalFlag == 2) {
                                submittedJustificationData = {
                                    annotation: initialresponse.data.id,
                                    temporal: true,
                                    claimPart: true,
                                    justification: justificationText
                                }
                            } else {
                                submittedJustificationData = {
                                    annotation: initialresponse.data.id,
                                    evidence: this.temporalJustificationEvidenceIds[i],
                                    temporal: true,
                                    claimPart: false,
                                    justification: justificationText
                                }
                            }
                            console.log(submittedJustificationData)

                            axios.post('/api/v1/database/annotation/add/justification/', submittedJustificationData).then(response => {
                                console.log(response.data)
                            }).catch(error => {
                                console.log(error)
                                // Request was made and server responded unfavourably
                                if (error.response.data.non_field_errors[0]) {
                                    this.toast.error(error.response.data.non_field_errors[0]);
                                }
                                // Request was made but no response received
                                else if (error.request) {
                                    this.toast.error("Received no response from the server. Please try again.");
                                }
                                // Something else happened
                                else {
                                    this.toast.error("Sorry, an unknown error occurred. Please try again.");
                                }
                            })

                        }

                        for (var i = 0; i < this.generalJustification.length; i++) {
                            const justificationText = this.generalJustification[i]
                            var submittedJustificationData;
                            // For claim justificaion, no need add evidence ids
                            if (this.generalFlag == 2) {
                                submittedJustificationData = {
                                    annotation: initialresponse.data.id,
                                    temporal: false,
                                    claimPart: true,
                                    justification: justificationText
                                }
                            } else {
                                submittedJustificationData = {
                                    annotation: initialresponse.data.id,
                                    evidence: this.generalJustificationEvidenceIds[i],
                                    temporal: false,
                                    claimPart: false,
                                    justification: justificationText
                                }
                            }
                            axios.post('/api/v1/database/annotation/add/justification/', submittedJustificationData).then(response => {
                                console.log(response.data)
                            }).catch(error => {
                                console.log(error.data)
                                // Request was made and server responded unfavourably
                                if (error.response.data.non_field_errors[0]) {
                                    this.toast.error(error.response.data.non_field_errors[0]);
                                }
                                // Request was made but no response received
                                else if (error.request) {
                                    this.toast.error("Received no response from the server. Please try again.");
                                }
                                // Something else happened
                                else {
                                    this.toast.error("Sorry, an unknown error occurred. Please try again.");
                                }
                            })
                        }
                    }
                    // Axios call to fetch first entry for annotation 
                    const annotateData = {
                        annotatorEmail: this.store.annotatorEmail,
                        databaseId: this.store.annotatingDatabase,
                    }
                    axios
                        .post('/api/v1/database/annotation/get/', annotateData)
                        .then(response => {
                            console.log(response.data)
                            this.annotationTodo = response.data.firstItem
                            this.count = response.data.count
                            this.section = 0;
                            this.overallTemporalFlag = 'true';
                            // Clears out previous entries
                            this.selectTemporal();
                            this.selectGeneral();
                        })
                        .catch(error => {
                            // Request was made and server responded unfavourably
                            if (error.response.data.non_field_errors[0]) {
                                this.toast.error(error.response.data.non_field_errors[0]);
                            }
                            // Request was made but no response received
                            else if (error.request) {
                                this.toast.error("Received no response from the server. Please try again.");
                            }
                            // Something else happened
                            else {
                                this.toast.error("Sorry, an unknown error occurred. Please try again.");
                            }
                        })
                })
                .catch(error => {
                    console.log(error)
                    // Request was made and server responded unfavourably
                    if (error.response.data.non_field_errors[0]) {
                        this.toast.error(error.response.data.non_field_errors[0]);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
        nextAnnotate() {
            // If last claim already, we simply submit the annotation
            if (this.count == 1) {
                this.submitAnnotation();
                this.count = 0;
                return
            }
            // Otherwise we submit the annotation and fetch the next claim
            this.submitAnnotation();
        },
    },
}
</script>

<style scoped>
.annotator {
    background-color: #f4f4f4;
    border-radius: 5px;
}

#annotating-label {
    font-size: 23px;
    font-weight: 700;
}

.move-on {
    font-size: 13px;
}

.submit {
    font-size: 18px;
    font-weight: 500;
    width: 380px;
    height: 70px;
}

.claim-badge {
    font-size: 16px;
    margin-bottom: 5px;
}

.claim-text {
    font-weight: 800;
}

.evidence-div {
    background-color: #f4f4f4;
    border: 1px solid #e1e0e0;
}

.label-badge {
    font-size: 18px;
    margin-bottom: 10px;
}

.label-button {
    font-size: 16px;
    font-weight: 800;
}

.annotation {
    border: 1px solid #e1e0e0;
}

.temporal_justification {
    width: 100%;
    height: 65px;
    background-color: #f4f4f4;
    border: 1px solid #e1e0e0;
    white-space: nowrap;
    overflow-x: auto;
}

.temporal-item {
    margin-left: 5px;
}

.annotate-next {
    font-size: 17px;
}

.annotate-next-button {
    width: 285px;
    height: 50px;
}

.annotate-next-button-2 {
    width: 255px;
    height: 65px;
}

.annotate-next-button-3 {
    width: 300px;
    height: 50px;
}

.home-button {
    width: 180px;
    height: 46px;
    font-size: 30px;
}
</style>
