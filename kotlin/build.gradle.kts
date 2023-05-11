import com.google.protobuf.gradle.generateProtoTasks
import com.google.protobuf.gradle.id
import com.google.protobuf.gradle.plugins
import com.google.protobuf.gradle.protobuf
import com.google.protobuf.gradle.protoc

//apply(plugin = "org.jetbrains.kotlin.jvm")

application {
    group = "com.remotivelabs.apis"
    version = "0.0.1-SNAPSHOT"
}

plugins {
    application
    kotlin("jvm") version "1.8.21"
    //kotlin("jvm")
    id("com.google.protobuf") version "0.8.19" // TODO: Does not work with 0.9.x.
}

dependencies {
//    protobuf(project(":protos"))

    api(kotlin("stdlib"))
    api("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4")
    api("io.grpc:grpc-stub:1.54.1")
    api("io.grpc:grpc-protobuf:1.54.1")
    api("com.google.protobuf:protobuf-java-util:3.22.3")
    api("com.google.protobuf:protobuf-kotlin:3.22.3")
    api("io.grpc:grpc-kotlin-stub:1.3.0")
}

repositories {
    mavenCentral()
}


// this makes it so IntelliJ picks up the sources but then ktlint complains

sourceSets {
    val main by getting { }
    main.java.srcDirs("build/generated/source/proto/main/java")
    main.java.srcDirs("build/generated/source/proto/main/grpc")
    main.java.srcDirs("build/generated/source/proto/main/kotlin")
    main.java.srcDirs("build/generated/source/proto/main/grpckt")
}


dependencies {
    protobuf(files("./tmp/protos"))
}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().all {
    kotlinOptions {
        freeCompilerArgs = listOf("-Xopt-in=kotlin.RequiresOptIn")
    }
}


protobuf {
    protoc {
        artifact = "com.google.protobuf:protoc:3.22.3"
    }
    plugins {
        id("grpc") {
            artifact = "io.grpc:protoc-gen-grpc-java:1.54.1"
        }
        id("grpckt") {
            artifact = "io.grpc:protoc-gen-grpc-kotlin:1.3.0:jdk8@jar"
        }
    }
    generateProtoTasks {
        all().forEach {
            it.plugins {
                id("grpc")
                id("grpckt")
            }
            it.builtins {
                id("kotlin")
            }
        }
    }
}